"""Create Task model — replaces WBSElement as operational unit."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("projects", "0002_project_new_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("wbs_code", models.CharField(db_index=True, help_text="WBS code, e.g., 3.1, 3.2.1", max_length=20)),
                ("name", models.CharField(max_length=255)),
                ("client_facing_label", models.CharField(blank=True, default="", max_length=255)),
                ("task_type", models.CharField(choices=[("TASK", "Tâche"), ("SUBTASK", "Sous-tâche")], default="TASK", max_length=10)),
                ("billing_mode", models.CharField(choices=[("FORFAIT", "Forfait"), ("HORAIRE", "Horaire"), ("POURCENTAGE", "Pourcentage")], default="FORFAIT", max_length=10)),
                ("order", models.PositiveIntegerField(default=0)),
                ("budgeted_hours", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("budgeted_cost", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("hourly_rate", models.DecimalField(blank=True, decimal_places=2, help_text="Hourly rate for HORAIRE billing mode", max_digits=8, null=True)),
                ("is_billable", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                ("parent", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="subtasks", to="projects.task")),
                ("phase", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="projects.phase")),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="projects.project")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="+", to="core.tenant")),
            ],
            options={
                "db_table": "projects_task",
                "ordering": ["phase__order", "order", "wbs_code"],
            },
        ),
        migrations.AddConstraint(
            model_name="task",
            constraint=models.UniqueConstraint(fields=("project", "wbs_code"), name="uq_task_project_wbs_code"),
        ),
    ]
