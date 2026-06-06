"""Nettoie la base locale en gardant uniquement users + tenants + paramètres.

Usage :
    docker exec erp-django-1 python manage.py shell < scripts/cleanup_data_keep_users_and_settings.py

Pour le mode dry-run, mettre DRY_RUN=True. Pour exécuter pour de vrai, mettre DRY_RUN=False.

Ce qui est PRÉSERVÉ :
- core: User, Tenant, ProjectRole, PositionProfile, TaxScheme, TaxRate,
        TaxConfiguration, LaborRule
- projects.ProjectTemplate (8 templates)
- expenses.ExpenseCategory
- leaves.LeaveType, LeaveBank, PublicHoliday
- billing.InvoiceTemplate, DunningLevel

Ce qui est SUPPRIMÉ :
- Tous les Historical* (audit trail)
- clients.Client + Contact + ClientAddress
- suppliers.ExternalOrganization + ST*
- projects.Project + Phase + Task + Amendment + SupportService
- time_entries.TimeEntry + WeeklyApproval + PeriodUnlock + PeriodFreeze + TimesheetLock
- billing.Invoice + InvoiceLine + CreditNote + Payment + Holdback + WriteOff
- expenses.ExpenseReport + ExpenseLine + ExpenseApproval
- consortiums.Consortium + ConsortiumMember
- leaves.LeaveRequest
- planning.ResourceAllocation + Milestone + VirtualResource + Availability + PlanningStandard
"""

import os  # noqa: E402

# Sécurité : DRY-RUN par défaut (aucune suppression). Pour exécuter réellement,
# lancer avec la variable d'environnement CLEANUP_EXECUTE=1.
DRY_RUN = os.environ.get("CLEANUP_EXECUTE") != "1"

from django.core.management import call_command  # noqa: E402
from django.db import transaction  # noqa: E402

from apps.billing.models import (  # noqa: E402
    CreditNote,
    Invoice,
    InvoiceLine,
    Payment,
)
from apps.clients.models import Client, ClientAddress, Contact  # noqa: E402
from apps.consortiums.models import Consortium, ConsortiumMember  # noqa: E402
from apps.expenses.models import ExpenseLine, ExpenseReport  # noqa: E402
from apps.leaves.models import LeaveRequest  # noqa: E402
from apps.planning.models import (  # noqa: E402
    Availability,
    Milestone,
    PlanningStandard,
    ResourceAllocation,
    VirtualResource,
)
from apps.projects.models import (  # noqa: E402
    Amendment,
    Phase,
    Project,
    SupportService,
    Task,
)
from apps.suppliers.models import ExternalOrganization  # noqa: E402
from apps.time_entries.models import (  # noqa: E402
    PeriodFreeze,
    PeriodUnlock,
    TimeEntry,
    TimesheetLock,
    WeeklyApproval,
)

# Ordre crucial: enfants avant parents pour FK ON DELETE PROTECT/RESTRICT
DELETION_ORDER = [
    # Time entries d'abord (FK vers Project, Phase, Task, Invoice, User)
    ("time_entries.PeriodUnlock", PeriodUnlock),
    ("time_entries.PeriodFreeze", PeriodFreeze),
    ("time_entries.TimesheetLock", TimesheetLock),
    ("time_entries.WeeklyApproval", WeeklyApproval),
    ("time_entries.TimeEntry", TimeEntry),
    # Planning (FK vers Project, Phase, Task, User, VirtualResource)
    ("planning.ResourceAllocation", ResourceAllocation),
    ("planning.Milestone", Milestone),
    ("planning.VirtualResource", VirtualResource),
    ("planning.Availability", Availability),
    ("planning.PlanningStandard", PlanningStandard),
    # Billing (FK vers Project, Client, ExternalOrganization)
    ("billing.Payment", Payment),
    ("billing.CreditNote", CreditNote),
    ("billing.InvoiceLine", InvoiceLine),
    ("billing.Invoice", Invoice),
    # Expenses (FK vers Project, ExpenseCategory, User)
    ("expenses.ExpenseLine", ExpenseLine),
    ("expenses.ExpenseReport", ExpenseReport),
    # Consortiums (FK vers Client, Project)
    ("consortiums.ConsortiumMember", ConsortiumMember),
    ("consortiums.Consortium", Consortium),
    # Leaves (FK vers User, LeaveType)
    ("leaves.LeaveRequest", LeaveRequest),
    # Projects (children avant Project)
    ("projects.Amendment", Amendment),
    ("projects.SupportService", SupportService),
    ("projects.Task", Task),
    ("projects.Phase", Phase),
    ("projects.Project", Project),
    # Clients
    ("clients.ClientAddress", ClientAddress),
    ("clients.Contact", Contact),
    ("clients.Client", Client),
    # Suppliers
    ("suppliers.ExternalOrganization", ExternalOrganization),
]


def main():
    print("=" * 60)
    print(f"CLEANUP DATA — DRY_RUN={DRY_RUN}")
    print("=" * 60)
    print()

    # 1. Compter avant
    print("Avant cleanup:")
    counts_before = {}
    total = 0
    for label, model in DELETION_ORDER:
        c = model.objects.count()
        counts_before[label] = c
        total += c
        if c > 0:
            print(f"  {label:45} : {c:>5}")
    print(f"  {'TOTAL':45} : {total:>5}")
    print()

    # 2. Suppression
    if DRY_RUN:
        print("DRY_RUN actif — aucune suppression effectuée.")
        print("Pour exécuter réellement : relancer avec CLEANUP_EXECUTE=1.")
        return

    print("Suppression en cours…")
    with transaction.atomic():
        for label, model in DELETION_ORDER:
            count = model.objects.count()
            if count == 0:
                continue
            deleted, _ = model.objects.all().delete()
            print(f"  ✔ {label:45} → {deleted} ligne(s) supprimées")

    # 3. Vérifier
    print()
    print("Après cleanup:")
    total_after = 0
    for label, model in DELETION_ORDER:
        c = model.objects.count()
        total_after += c
        if c > 0:
            print(f"  {label:45} : {c:>5}  ⚠ RESTE")
    print(f"  {'TOTAL':45} : {total_after:>5}")

    # 4bis. Re-création du jeu de phases standard (paramétrage)
    print()
    print("Re-seed des phases standard (paramétrage)…")
    call_command("seed_standard_phases")

    # 4ter. Re-création du projet interne + tâches obligatoires de la feuille
    # de temps (Congés/Formation/Maladie). Sans ça, la grille de saisie perd
    # ses lignes obligatoires après nettoyage.
    print("Re-seed du projet interne + tâches obligatoires…")
    call_command("seed_internal_mandatory_tasks")

    # 4. Récap des éléments PRÉSERVÉS
    from django.contrib.auth import get_user_model

    from apps.billing.models import DunningLevel, InvoiceTemplate
    from apps.core.models import (
        LaborRule,
        PositionProfile,
        ProjectRole,
        TaxConfiguration,
        TaxRate,
        TaxScheme,
        Tenant,
    )
    from apps.expenses.models import ExpenseCategory
    from apps.leaves.models import LeaveBank, LeaveType, PublicHoliday
    from apps.projects.models import ProjectTemplate, StandardPhase

    print()
    print("Préservés :")
    user_model = get_user_model()
    for label, model in [
        ("Users", user_model),
        ("core.Tenant", Tenant),
        ("core.ProjectRole", ProjectRole),
        ("core.PositionProfile", PositionProfile),
        ("core.TaxScheme", TaxScheme),
        ("core.TaxRate", TaxRate),
        ("core.TaxConfiguration", TaxConfiguration),
        ("core.LaborRule", LaborRule),
        ("projects.ProjectTemplate", ProjectTemplate),
        ("projects.StandardPhase", StandardPhase),
        ("expenses.ExpenseCategory", ExpenseCategory),
        ("leaves.LeaveType", LeaveType),
        ("leaves.LeaveBank", LeaveBank),
        ("leaves.PublicHoliday", PublicHoliday),
        ("billing.InvoiceTemplate", InvoiceTemplate),
        ("billing.DunningLevel", DunningLevel),
    ]:
        c = model.objects.count()
        print(f"  {label:30} : {c:>4}")


main()
