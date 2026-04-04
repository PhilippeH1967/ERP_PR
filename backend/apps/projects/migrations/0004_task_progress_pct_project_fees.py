"""Add progress_pct to Task, add fee fields to Project + HistoricalProject."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_create_task_model"),
    ]

    operations = [
        # Task: progress_pct
        migrations.AddField(
            model_name="task",
            name="progress_pct",
            field=models.DecimalField(decimal_places=2, default=0, help_text="Manual progress percentage 0-100", max_digits=5),
        ),
        # Project: fee fields
        migrations.AddField(
            model_name="project",
            name="total_fees",
            field=models.DecimalField(blank=True, decimal_places=2, help_text="Total honoraires HT", max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="fee_calculation_method",
            field=models.CharField(blank=True, choices=[("FORFAIT", "Forfait"), ("COUT_TRAVAUX", "Coût des travaux %"), ("HORAIRE", "Horaire")], default="FORFAIT", max_length=20),
        ),
        migrations.AddField(
            model_name="project",
            name="fee_rate_pct",
            field=models.DecimalField(blank=True, decimal_places=2, help_text="Percentage of construction cost", max_digits=5, null=True),
        ),
        # HistoricalProject: same fee fields
        migrations.AddField(
            model_name="historicalproject",
            name="total_fees",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name="historicalproject",
            name="fee_calculation_method",
            field=models.CharField(blank=True, choices=[("FORFAIT", "Forfait"), ("COUT_TRAVAUX", "Coût des travaux %"), ("HORAIRE", "Horaire")], default="FORFAIT", max_length=20),
        ),
        migrations.AddField(
            model_name="historicalproject",
            name="fee_rate_pct",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
