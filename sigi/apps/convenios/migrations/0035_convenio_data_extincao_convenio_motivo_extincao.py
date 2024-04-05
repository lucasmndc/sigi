# Generated by Django 4.2.11 on 2024-04-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("convenios", "0034_gescon_checksums"),
    ]

    operations = [
        migrations.AddField(
            model_name="convenio",
            name="data_extincao",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="data de extinção/desistência",
            ),
        ),
        migrations.AddField(
            model_name="convenio",
            name="motivo_extincao",
            field=models.TextField(
                blank=True, verbose_name="motivo da extinção/desistência"
            ),
        ),
    ]