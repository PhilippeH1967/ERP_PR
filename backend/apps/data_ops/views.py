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
    # Reference data (import first)
    {
        "key": "ref_profils_poste",
        "label": "Profils de poste",
        "description": "31 archetypes (Architecte, Urbaniste, Designer...)",
        "file": "R1_profils_poste.xlsx",
        "order": 0.1,
        "icon": "🎓",
        "category": "reference",
    },
    {
        "key": "ref_categories_depenses",
        "label": "Catégories de dépenses",
        "description": "Transport, Repas, Hébergement, Fournitures... avec codes GL",
        "file": "R2_categories_depenses.xlsx",
        "order": 0.2,
        "icon": "🏷️",
        "category": "reference",
    },
    {
        "key": "ref_templates_projet",
        "label": "Templates de projet",
        "description": "1 par type contrat avec phases pré-configurées",
        "file": "R3_templates_projet.xlsx",
        "order": 0.3,
        "icon": "📋",
        "category": "reference",
    },
    {
        "key": "ref_templates_facture",
        "label": "Templates de facture",
        "description": "Formats de facture (Standard, Ville, Fédéral...)",
        "file": "R4_templates_facture.xlsx",
        "order": 0.4,
        "icon": "🧾",
        "category": "reference",
    },
    {
        "key": "ref_niveaux_relance",
        "label": "Niveaux de relance",
        "description": "3 niveaux : 30j courtois, 60j rappel, 90j mise en demeure",
        "file": "R5_niveaux_relance.xlsx",
        "order": 0.5,
        "icon": "📨",
        "category": "reference",
    },
    {
        "key": "ref_unites_affaires",
        "label": "Unités d'affaires",
        "description": "Architecture, Design, Urbanisme, etc.",
        "file": "R6_unites_affaires.xlsx",
        "order": 0.6,
        "icon": "🏗️",
        "category": "reference",
    },
    # Transactional data
    {
        "key": "employes",
        "label": "Employés",
        "description": "Utilisateurs avec rôles, BU, profil de poste",
        "file": "01_employes.xlsx",
        "order": 1,
        "icon": "👥",
        "category": "data",
    },
    {
        "key": "clients",
        "label": "Clients, Contacts & Adresses",
        "description": "Clients avec contacts et adresses (3 onglets)",
        "file": "02_clients.xlsx",
        "order": 2,
        "icon": "🏢",
        "category": "data",
    },
    {
        "key": "sous_traitants",
        "label": "Sous-traitants / Organisations",
        "description": "Registre partagé des organisations externes",
        "file": "05_sous_traitants.xlsx",
        "order": 3,
        "icon": "🤝",
        "category": "data",
    },
    {
        "key": "projets",
        "label": "Projets, Phases & WBS",
        "description": "Projets avec phases et structure WBS (3 onglets)",
        "file": "03_projets.xlsx",
        "order": 4,
        "icon": "📁",
        "category": "data",
    },
    {
        "key": "feuilles_de_temps",
        "label": "Feuilles de temps",
        "description": "Entrées de temps par employé/projet/phase/date",
        "file": "04_feuilles_de_temps.xlsx",
        "order": 5,
        "icon": "⏱️",
        "category": "data",
    },
    {
        "key": "factures_fournisseurs",
        "label": "Factures fournisseurs (ST)",
        "description": "Import en masse des factures sous-traitants avec projet, montant, statut",
        "file": "06_factures_fournisseurs.xlsx",
        "order": 6,
        "icon": "📑",
        "category": "data",
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
        tenant_id = getattr(request, "tenant_id", None)
        if not tenant_id:
            return Response(
                {"error": {"code": "NO_TENANT", "message": "Tenant requis (X-Tenant-Id)", "details": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from apps.core.models import Tenant

        tenant = Tenant.objects.get(pk=tenant_id)

        # Special handler for ST invoice import
        if import_key == "factures_fournisseurs":
            result = _import_st_invoices(tmp_path, tenant)
            return Response({"status": "success", "import_type": import_key, "output": result})

        # Generic handler via management command
        from django.core.management import call_command
        from io import StringIO

        out = StringIO()
        folder = os.path.dirname(tmp_path)

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
        for f in [tmp_path]:
            if os.path.exists(f):
                os.unlink(f)
        expected_path_local = os.path.join(os.path.dirname(tmp_path), import_type.get("file", ""))
        if os.path.exists(expected_path_local):
            os.unlink(expected_path_local)


def _import_st_invoices(filepath, tenant):
    """Import ST invoices from Excel template."""
    import openpyxl

    from apps.projects.models import Project
    from apps.suppliers.models import ExternalOrganization, STInvoice

    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb.active

    created = 0
    skipped = 0
    errors = []

    for row_num, row in enumerate(ws.iter_rows(min_row=3, values_only=True), 3):
        if not row or not row[0]:
            continue

        no_facture = str(row[0]).strip()
        nom_fournisseur = str(row[1] or "").strip()
        code_projet = str(row[2] or "").strip()
        date_facture = row[3]
        montant = row[4]
        statut = str(row[6] or "received").strip().lower()
        description = str(row[7] or "").strip()

        if not no_facture or not nom_fournisseur or not code_projet:
            errors.append(f"Ligne {row_num}: champs obligatoires manquants")
            continue

        # Find supplier
        try:
            supplier = ExternalOrganization.objects.get(
                tenant=tenant, name__iexact=nom_fournisseur
            )
        except ExternalOrganization.DoesNotExist:
            errors.append(f"Ligne {row_num}: fournisseur '{nom_fournisseur}' introuvable")
            continue

        # Find project
        try:
            project = Project.objects.get(tenant=tenant, code=code_projet)
        except Project.DoesNotExist:
            errors.append(f"Ligne {row_num}: projet '{code_projet}' introuvable")
            continue

        # Check duplicate
        if STInvoice.objects.filter(
            tenant=tenant, invoice_number=no_facture, supplier=supplier
        ).exists():
            skipped += 1
            continue

        # Parse date
        if hasattr(date_facture, "date"):
            date_facture = date_facture.date()
        elif isinstance(date_facture, str):
            from datetime import datetime

            date_facture = datetime.strptime(date_facture[:10], "%Y-%m-%d").date()

        # Validate status
        if statut not in ("received", "authorized", "paid"):
            statut = "received"

        STInvoice.objects.create(
            tenant=tenant,
            supplier=supplier,
            project=project,
            invoice_number=no_facture,
            invoice_date=date_facture,
            amount=float(montant or 0),
            status=statut,
            source="api",
        )
        created += 1

    wb.close()
    result = f"Import terminé: {created} factures créées, {skipped} doublons ignorés"
    if errors:
        result += f"\n{len(errors)} erreurs:\n" + "\n".join(errors[:20])
    return result
