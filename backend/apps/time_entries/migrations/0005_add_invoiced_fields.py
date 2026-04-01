"""Add is_invoiced and invoiced_on fields to TimeEntry and HistoricalTimeEntry."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
        ("time_entries", "0004_add_period_freeze"),
    ]

    operations = [
        # TimeEntry
        migrations.AddField(
            model_name="timeentry",
            name="is_invoiced",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="timeentry",
            name="invoiced_on",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoiced_entries",
                to="billing.invoice",
            ),
        ),
        # HistoricalTimeEntry
        migrations.AddField(
            model_name="historicaltimeentry",
            name="is_invoiced",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="historicaltimeentry",
            name="invoiced_on",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="billing.invoice",
                db_constraint=False,
            ),
        ),
    ]
