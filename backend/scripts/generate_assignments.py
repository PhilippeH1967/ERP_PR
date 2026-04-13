import django, os
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
django.setup()

from apps.projects.models import Project, EmployeeAssignment
from apps.time_entries.models import TimeEntry
from apps.core.models import Tenant

tenant = Tenant.objects.get(id=1)
created = 0
for project in Project.objects.filter(tenant=tenant):
    combos = TimeEntry.objects.filter(project=project).values("employee", "phase").distinct()
    for combo in combos:
        emp_id = combo["employee"]
        phase_id = combo["phase"]
        if not emp_id:
            continue
        exists = EmployeeAssignment.objects.filter(tenant=tenant, project=project, employee_id=emp_id, phase_id=phase_id).exists()
        if not exists:
            EmployeeAssignment.objects.create(tenant=tenant, project=project, employee_id=emp_id, phase_id=phase_id, percentage="100")
            created += 1
print(f"Done: {created} affectations creees")
