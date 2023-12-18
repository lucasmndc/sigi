# Generated by Django 4.2.4 on 2023-12-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventos", "0055_evento_reserva"),
    ]

    operations = [
        migrations.AddField(
            model_name="evento",
            name="origem_sincronizacao",
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name="origem da sincronização",
            ),
        ),
    ]
