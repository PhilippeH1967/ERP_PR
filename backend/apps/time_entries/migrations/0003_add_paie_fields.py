"""Add PAIE role fields to WeeklyApproval and PAIE_VALIDATED status to TimeEntry."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("time_entries", "0002_add_rejection_reason"),
    ]

    operations = [
        # Add paie fields to WeeklyApproval
        migrations.AddField(
            model_name="weeklyapproval",
            name="paie_status",
            field=models.CharField(
                choices=[("PENDING", "En attente"), ("APPROVED", "Approuvé"), ("REJECTED", "Rejeté")],
                default="PENDING",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="weeklyapproval",
            name="paie_validated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="paie_validations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="weeklyapproval",
            name="paie_validated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        # TimeEntry status choices update is handled by Django automatically
        # (TextChoices changes don't need migration for CharField)
    ]
