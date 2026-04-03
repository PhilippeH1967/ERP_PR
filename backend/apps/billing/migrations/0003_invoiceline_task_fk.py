"""Add task FK to InvoiceLine (replaces financial_phase for WBS Option B)."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_create_task_model"),
        ("billing", "0002_invoice_project_nullable"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoiceline",
            name="task",
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoice_lines",
                to="projects.task",
            ),
        ),
    ]
