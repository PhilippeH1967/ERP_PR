"""Drop EmployeeAssignment — planning unifié sur ResourceAllocation."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_task_end_date_task_start_date"),
        ("planning", "0004_migrate_employee_assignments"),
    ]

    operations = [
        migrations.DeleteModel(name="EmployeeAssignment"),
    ]
