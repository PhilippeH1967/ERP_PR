"""Payroll validation controls for PAIE role."""

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum


def run_controls(employee, week_start, week_end, entries, all_entries_qs):
    """Run all payroll controls for one employee/week. Returns list of alerts."""
    alerts = []
    contract_hours = 40  # TODO: from employee profile
    OVERTIME_THRESHOLD = contract_hours

    # Group entries by date
    by_date = defaultdict(list)
    for e in entries:
        by_date[e.date].append(e)

    total_hours = sum(float(e.hours) for e in entries)

    # Categorize hours
    # We use project.is_internal to detect non-project hours
    # Absence categories detected by project name patterns
    absence_keywords = {"maladie", "sick", "conge", "congé", "vacance", "vacation", "ferie", "férié", "personnel"}
    sick_keywords = {"maladie", "sick"}

    sick_hours = 0
    leave_hours = 0
    for e in entries:
        proj_name = (e.project.name or "").lower()
        if any(k in proj_name for k in sick_keywords):
            sick_hours += float(e.hours)
        elif any(k in proj_name for k in absence_keywords):
            leave_hours += float(e.hours)

    overtime = max(0, total_hours - OVERTIME_THRESHOLD)

    # ============================================================
    # CONTROL 1: Heures incomplètes
    # ============================================================
    if total_hours < contract_hours and (sick_hours + leave_hours) == 0:
        deficit = contract_hours - total_hours
        alerts.append({
            "code": "INCOMPLETE_HOURS",
            "severity": "warning",
            "message": f"{total_hours}h saisies sur {contract_hours}h contractuelles — {deficit}h manquantes sans absence déclarée",
        })

    # ============================================================
    # CONTROL 2: Heures sup + maladie même semaine
    # ============================================================
    if overtime > 0 and sick_hours > 0:
        alerts.append({
            "code": "OVERTIME_WITH_SICK",
            "severity": "error",
            "message": f"{overtime}h supplémentaires déclarées avec {sick_hours}h de maladie la même semaine — interdit",
        })

    # ============================================================
    # CONTROL 3: Heures sup + congé même semaine
    # ============================================================
    if overtime > 0 and leave_hours > 0:
        effective_threshold = contract_hours - leave_hours
        real_work_hours = total_hours - leave_hours
        if real_work_hours > effective_threshold:
            real_overtime = real_work_hours - effective_threshold
            alerts.append({
                "code": "OVERTIME_WITH_LEAVE",
                "severity": "warning",
                "message": f"{leave_hours}h de congé + {real_overtime}h supplémentaires — le seuil d'heures sup est de {effective_threshold}h cette semaine",
            })

    # ============================================================
    # CONTROL 4: Heures supplémentaires non autorisées (> contrat)
    # ============================================================
    if overtime > 0 and sick_hours == 0 and leave_hours == 0:
        severity = "error" if overtime > 10 else "warning"
        alerts.append({
            "code": "OVERTIME",
            "severity": severity,
            "message": f"{overtime}h supplémentaires ({total_hours}h total vs {contract_hours}h contrat)",
        })

    # ============================================================
    # CONTROL 5: Journée > 10h
    # ============================================================
    for date, day_entries in by_date.items():
        day_total = sum(float(e.hours) for e in day_entries)
        if day_total > 10:
            alerts.append({
                "code": "DAY_OVER_10H",
                "severity": "warning",
                "message": f"{date.strftime('%A %d/%m')} : {day_total}h déclarées (max recommandé: 10h)",
            })

    # ============================================================
    # CONTROL 6: Weekend travaillé
    # ============================================================
    for date, day_entries in by_date.items():
        if date.weekday() >= 5:  # Saturday=5, Sunday=6
            day_total = sum(float(e.hours) for e in day_entries)
            if day_total > 0:
                day_name = "samedi" if date.weekday() == 5 else "dimanche"
                alerts.append({
                    "code": "WEEKEND_WORK",
                    "severity": "warning",
                    "message": f"{day_total}h travaillées le {day_name} {date.strftime('%d/%m')}",
                })

    # ============================================================
    # CONTROL 7: Maladie + heures sur même journée
    # ============================================================
    for date, day_entries in by_date.items():
        has_sick = any(any(k in (e.project.name or "").lower() for k in sick_keywords) for e in day_entries)
        has_work = any(not any(k in (e.project.name or "").lower() for k in absence_keywords) for e in day_entries)
        if has_sick and has_work:
            work_hrs = sum(float(e.hours) for e in day_entries if not any(k in (e.project.name or "").lower() for k in absence_keywords))
            sick_hrs = sum(float(e.hours) for e in day_entries if any(k in (e.project.name or "").lower() for k in sick_keywords))
            if work_hrs > 0 and sick_hrs > 0:
                alerts.append({
                    "code": "SICK_AND_WORK_SAME_DAY",
                    "severity": "error",
                    "message": f"{date.strftime('%d/%m')} : {sick_hrs}h maladie et {work_hrs}h de travail la même journée",
                })

    # ============================================================
    # CONTROL 8: Tendance inhabituelle (> 20% écart vs moyenne 4 sem.)
    # ============================================================
    trend_totals = []
    for w in range(4, 0, -1):
        ws = week_start - timedelta(weeks=w)
        we = ws + timedelta(days=6)
        wt = all_entries_qs.filter(
            date__gte=ws, date__lte=we,
        ).aggregate(t=Sum("hours"))["t"] or Decimal("0")
        trend_totals.append(float(wt))

    if any(t > 0 for t in trend_totals):
        avg = sum(trend_totals) / max(1, sum(1 for t in trend_totals if t > 0))
        if avg > 0 and abs(total_hours - avg) / avg > 0.20:
            direction = "supérieur" if total_hours > avg else "inférieur"
            alerts.append({
                "code": "UNUSUAL_TREND",
                "severity": "info",
                "message": f"{total_hours}h cette semaine — {direction} de {abs(round(total_hours - avg, 1))}h par rapport à la moyenne ({round(avg, 1)}h)",
            })

    # ============================================================
    # CONTROL 9: Heures sup consécutives (3+ semaines)
    # ============================================================
    consecutive_overtime = 0
    for w in range(4, 0, -1):
        ws = week_start - timedelta(weeks=w)
        we = ws + timedelta(days=6)
        wt = float(all_entries_qs.filter(
            date__gte=ws, date__lte=we,
        ).aggregate(t=Sum("hours"))["t"] or Decimal("0"))
        if wt > contract_hours:
            consecutive_overtime += 1
        else:
            consecutive_overtime = 0
    # Current week
    if total_hours > contract_hours:
        consecutive_overtime += 1
    if consecutive_overtime >= 3:
        alerts.append({
            "code": "CONSECUTIVE_OVERTIME",
            "severity": "error",
            "message": f"{consecutive_overtime} semaines consécutives avec heures supplémentaires — risque burn-out",
        })

    # ============================================================
    # CONTROL 10: Approbation CP incomplète
    # ============================================================
    statuses = [e.status for e in entries]
    submitted_not_approved = sum(1 for s in statuses if s == "SUBMITTED")
    if submitted_not_approved > 0:
        alerts.append({
            "code": "PM_NOT_APPROVED",
            "severity": "error",
            "message": f"{submitted_not_approved} entrée(s) soumise(s) mais non encore approuvée(s) par le CP",
        })

    # ============================================================
    # CONTROL 11: Maximum légal 50h (LNT Québec)
    # ============================================================
    if total_hours > 50:
        alerts.append({
            "code": "LEGAL_MAX_50H",
            "severity": "error",
            "message": f"{total_hours}h dépasse le maximum légal de 50h/semaine (LNT Québec)",
        })

    return alerts
