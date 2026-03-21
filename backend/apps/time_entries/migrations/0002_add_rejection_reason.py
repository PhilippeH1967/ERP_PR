# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_entries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='rejection_reason',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='historicaltimeentry',
            name='rejection_reason',
            field=models.TextField(blank=True, default=''),
        ),
    ]
