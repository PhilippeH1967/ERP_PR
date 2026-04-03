"""Add location, surface, currency, tags, title_on_invoice to Project."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        # Location fields
        migrations.AddField(
            model_name="project",
            name="address",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="project",
            name="city",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="project",
            name="postal_code",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="project",
            name="country",
            field=models.CharField(blank=True, default="Canada", max_length=100),
        ),
        # Project details
        migrations.AddField(
            model_name="project",
            name="surface",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="surface_unit",
            field=models.CharField(
                blank=True, choices=[("m2", "m²"), ("pi2", "pi²")], default="m2", max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="currency",
            field=models.CharField(blank=True, default="CAD", max_length=3),
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="project",
            name="title_on_invoice",
            field=models.CharField(
                blank=True, default="", help_text="Titre affiché sur les factures", max_length=255,
            ),
        ),
        # Historical model fields
        migrations.AddField(model_name="historicalproject", name="address", field=models.CharField(blank=True, default="", max_length=255)),
        migrations.AddField(model_name="historicalproject", name="city", field=models.CharField(blank=True, default="", max_length=100)),
        migrations.AddField(model_name="historicalproject", name="postal_code", field=models.CharField(blank=True, default="", max_length=20)),
        migrations.AddField(model_name="historicalproject", name="country", field=models.CharField(blank=True, default="Canada", max_length=100)),
        migrations.AddField(model_name="historicalproject", name="surface", field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
        migrations.AddField(model_name="historicalproject", name="surface_unit", field=models.CharField(blank=True, choices=[("m2", "m²"), ("pi2", "pi²")], default="m2", max_length=5)),
        migrations.AddField(model_name="historicalproject", name="currency", field=models.CharField(blank=True, default="CAD", max_length=3)),
        migrations.AddField(model_name="historicalproject", name="tags", field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name="historicalproject", name="title_on_invoice", field=models.CharField(blank=True, default="", max_length=255)),
    ]
