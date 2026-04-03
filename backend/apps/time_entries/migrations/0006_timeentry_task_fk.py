"""Add task FK to TimeEntry (replaces phase for WBS Option B)."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_create_task_model"),
        ("time_entries", "0005_add_invoiced_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="timeentry",
            name="task",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="time_entries",
                to="projects.task",
            ),
        ),
        migrations.AddField(
            model_name="historicaltimeentry",
            name="task",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="projects.task",
                db_constraint=False,
            ),
        ),
    ]
