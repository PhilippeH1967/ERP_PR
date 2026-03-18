"""Data import/export API views."""

import os
import tempfile

from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "import_templates")

IMPORT_TYPES = [
    {
        "key": "employes",
        "label": "Employés",
        "description": "Utilisateurs avec rôles, BU, profil de poste",
        "file": "01_employes.xlsx",
        "order": 1,
        "icon": "👥",
    },
    {
        "key": "clients",
        "label": "Clients, Contacts & Adresses",
        "description": "Clients avec contacts et adresses (3 onglets)",
        "file": "02_clients.xlsx",
        "order": 2,
        "icon": "🏢",
    },
    {
        "key": "sous_traitants",
        "label": "Sous-traitants / Organisations",
        "description": "Registre partagé des organisations externes",
        "file": "05_sous_traitants.xlsx",
        "order": 3,
        "icon": "🤝",
    },
    {
        "key": "projets",
        "label": "Projets, Phases & WBS",
        "description": "Projets avec phases et structure WBS (3 onglets)",
        "file": "03_projets.xlsx",
        "order": 4,
        "icon": "📁",
    },
    {
        "key": "feuilles_de_temps",
        "label": "Feuilles de temps",
        "description": "Entrées de temps par employé/projet/phase/date",
        "file": "04_feuilles_de_temps.xlsx",
        "order": 5,
        "icon": "⏱️",
    },
]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_import_types(request):
    """List all available import types with template download info."""
    return Response({"import_types": IMPORT_TYPES})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_template(request, import_key):
    """Download Excel template for a specific import type."""
    import_type = next((t for t in IMPORT_TYPES if t["key"] == import_key), None)
    if not import_type:
        return Response(
            {"error": {"code": "NOT_FOUND", "message": "Type d'import inconnu", "details": []}},
            status=status.HTTP_404_NOT_FOUND,
        )

    filepath = os.path.join(TEMPLATES_DIR, import_type["file"])
    if not os.path.exists(filepath):
        return Response(
            {"error": {"code": "FILE_NOT_FOUND", "message": "Template non disponible", "details": []}},
            status=status.HTTP_404_NOT_FOUND,
        )

    return FileResponse(
        open(filepath, "rb"),
        as_attachment=True,
        filename=import_type["file"],
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_import(request, import_key):
    """Upload and process an Excel import file."""
    import_type = next((t for t in IMPORT_TYPES if t["key"] == import_key), None)
    if not import_type:
        return Response(
            {"error": {"code": "NOT_FOUND", "message": "Type d'import inconnu", "details": []}},
            status=status.HTTP_404_NOT_FOUND,
        )

    file = request.FILES.get("file")
    if not file:
        return Response(
            {"error": {"code": "NO_FILE", "message": "Aucun fichier fourni", "details": []}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not file.name.endswith((".xlsx", ".xls")):
        return Response(
            {"error": {"code": "INVALID_FORMAT", "message": "Format Excel requis (.xlsx)", "details": []}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        for chunk in file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        from django.core.management import call_command
        from io import StringIO

        tenant_id = getattr(request, "tenant_id", None)
        if not tenant_id:
            return Response(
                {"error": {"code": "NO_TENANT", "message": "Tenant requis (X-Tenant-Id)", "details": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from apps.core.models import Tenant

        tenant = Tenant.objects.get(pk=tenant_id)

        # Run import command with the uploaded file's folder
        out = StringIO()
        folder = os.path.dirname(tmp_path)

        # Rename temp file to expected name
        expected_name = import_type["file"]
        expected_path = os.path.join(folder, expected_name)
        os.rename(tmp_path, expected_path)

        call_command(
            "import_changepoint",
            folder,
            tenant=tenant.slug,
            stdout=out,
        )

        output = out.getvalue()

        return Response({
            "status": "success",
            "import_type": import_key,
            "output": output,
        })

    except Exception as e:
        return Response(
            {"error": {"code": "IMPORT_ERROR", "message": str(e), "details": []}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        # Cleanup
        for f in [tmp_path, expected_path]:
            if os.path.exists(f):
                os.unlink(f)
