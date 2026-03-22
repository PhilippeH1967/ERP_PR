"""Add PeriodFreeze model for global freeze date."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
        ("time_entries", "0003_add_paie_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="PeriodFreeze",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("freeze_before", models.DateField(help_text="No time entries can be created or modified before this date.")),
                ("frozen_at", models.DateTimeField(auto_now_add=True)),
                ("frozen_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="period_freezes", to=settings.AUTH_USER_MODEL)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="+", to="core.tenant")),
            ],
            options={
                "db_table": "time_entries_period_freeze",
                "ordering": ["-frozen_at"],
            },
        ),
    ]
