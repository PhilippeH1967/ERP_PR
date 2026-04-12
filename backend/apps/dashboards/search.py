"""Global search endpoint for Cmd+K (Sprint 2 - B3)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def global_search(request):
    """Search across projects, clients, invoices, users."""
    q = request.query_params.get("q", "").strip()
    search_type = request.query_params.get("type", "")
    tenant_id = getattr(request, "tenant_id", None)

    if not q or len(q) < 2:
        return Response({"data": {"results": [], "total": 0}})

    results = []
    q_lower = q.lower()

    def score(text):
        t = text.lower()
        if t == q_lower:
            return 0
        if t.startswith(q_lower):
            return 1
        return 2

    # Projects
    if not search_type or search_type == "project":
        from apps.projects.models import Project
        qs = Project.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        for p in qs.filter(name__icontains=q)[:10]:
            results.append({
                "type": "project", "id": p.id,
                "title": f"{p.code} — {p.name}",
                "subtitle": p.get_status_display() if hasattr(p, 'get_status_display') else p.status,
                "url": f"/projects/{p.id}",
                "_score": score(p.name),
            })
        for p in qs.filter(code__icontains=q).exclude(name__icontains=q)[:5]:
            results.append({
                "type": "project", "id": p.id,
                "title": f"{p.code} — {p.name}",
                "subtitle": p.status,
                "url": f"/projects/{p.id}",
                "_score": score(p.code),
            })

    # Clients
    if not search_type or search_type == "client":
        from apps.clients.models import Client
        qs = Client.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        for c in qs.filter(name__icontains=q)[:10]:
            results.append({
                "type": "client", "id": c.id,
                "title": c.name,
                "subtitle": c.alias or "",
                "url": f"/clients/{c.id}",
                "_score": score(c.name),
            })

    # Invoices
    if not search_type or search_type == "invoice":
        from apps.billing.models import Invoice
        qs = Invoice.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        for inv in qs.filter(invoice_number__icontains=q)[:10]:
            results.append({
                "type": "invoice", "id": inv.id,
                "title": f"Facture {inv.invoice_number}",
                "subtitle": f"{inv.status} — {inv.total_amount} $",
                "url": f"/billing/{inv.id}",
                "_score": score(inv.invoice_number),
            })

    # Users/Employees
    if not search_type or search_type == "employee":
        from django.contrib.auth.models import User
        for u in User.objects.filter(first_name__icontains=q)[:5]:
            results.append({
                "type": "employee", "id": u.id,
                "title": f"{u.first_name} {u.last_name}".strip() or u.username,
                "subtitle": u.email,
                "url": f"/admin/users",
                "_score": score(u.first_name),
            })
        for u in User.objects.filter(last_name__icontains=q).exclude(first_name__icontains=q)[:5]:
            results.append({
                "type": "employee", "id": u.id,
                "title": f"{u.first_name} {u.last_name}".strip() or u.username,
                "subtitle": u.email,
                "url": f"/admin/users",
                "_score": score(u.last_name),
            })

    # Sort by score then limit
    results.sort(key=lambda r: r["_score"])
    for r in results:
        r.pop("_score", None)

    return Response({"data": {"results": results[:20], "total": len(results)}})
