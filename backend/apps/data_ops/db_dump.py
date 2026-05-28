"""Admin DB dump endpoint — wraps pg_dump for support/debug downloads."""

import logging
import os
import subprocess
from datetime import UTC, datetime

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.core.permissions import IsAdmin

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([IsAdmin])
def db_dump(request):
    """Stream a pg_dump (custom format) of the current database to the
    authenticated admin. Used to mirror a remote (Hostinger) state into a
    local dev/test environment for diagnosis.

    Custom format (-Fc) → directly restorable with pg_restore, compressed,
    no need for an extra gzip step.
    """
    db = settings.DATABASES["default"]
    env = os.environ.copy()
    env["PGPASSWORD"] = db.get("PASSWORD", "") or ""

    cmd = [
        "pg_dump",
        "-Fc",
        "-h",
        db.get("HOST") or "localhost",
        "-p",
        str(db.get("PORT") or 5432),
        "-U",
        db.get("USER") or "",
        "-d",
        db.get("NAME") or "",
    ]

    try:
        proc = subprocess.Popen(  # noqa: S603 — args are fixed binary + settings
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        logger.exception("pg_dump binary not available")
        return Response(
            {
                "error": {
                    "code": "PG_DUMP_MISSING",
                    "message": (
                        "pg_dump introuvable dans le conteneur. Reconstruis "
                        "l'image Django (le Dockerfile installe postgresql-client-16)."
                    ),
                }
            },
            status=500,
        )

    # Peek the first chunk to surface obvious failures before we send headers.
    assert proc.stdout is not None  # noqa: S101 — pipe always opens; guard for type checkers
    first = proc.stdout.read(8)
    if not first:
        err = (proc.stderr.read() if proc.stderr else b"").decode("utf-8", errors="replace")
        proc.wait()
        logger.error("pg_dump produced no output: %s", err[:500])
        return Response(
            {"error": {"code": "PG_DUMP_FAILED", "message": err[:500] or "pg_dump failed"}},
            status=500,
        )

    def stream():
        try:
            yield first
            while True:
                chunk = proc.stdout.read(65536)
                if not chunk:
                    break
                yield chunk
        finally:
            if proc.stdout:
                proc.stdout.close()
            if proc.stderr:
                proc.stderr.close()
            proc.wait()

    ts = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    db_name = db.get("NAME") or "erp"
    filename = f"{db_name}-{ts}.dump"
    response = StreamingHttpResponse(stream(), content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# Compatibility: DRF Response import unused when only StreamingHttpResponse is
# returned on success; keep the import for the error paths above.
_ = HttpResponse
