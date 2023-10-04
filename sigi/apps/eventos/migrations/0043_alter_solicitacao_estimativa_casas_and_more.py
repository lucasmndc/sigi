# Generated by Django 4.2.4 on 2023-09-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventos", "0042_atualiza_status_solicitacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solicitacao",
            name="estimativa_casas",
            field=models.PositiveIntegerField(
                default=0,
                help_text="estimativa de quantas Casas participarão dos eventos",
                verbose_name="estimativa de Casas participantes",
            ),
        ),
        migrations.AlterField(
            model_name="solicitacao",
            name="estimativa_servidores",
            field=models.PositiveIntegerField(
                default=0,
                help_text="estimativa de quantos Servidores participarão dos eventos",
                verbose_name="estimativa de servidores participantes",
            ),
        ),
    ]