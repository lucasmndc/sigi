# Generated by Django 4.2.4 on 2023-10-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventos", "0051_ajusta_status_evento"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evento",
            name="status",
            field=models.CharField(
                choices=[
                    ("P", "Previto"),
                    ("O", "Autorizado"),
                    ("R", "Realizado"),
                    ("C", "Cancelado"),
                    ("Q", "Sobrestado"),
                ],
                max_length=1,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="itemsolicitado",
            name="status",
            field=models.CharField(
                choices=[
                    ("S", "Solicitado"),
                    ("A", "Autorizado"),
                    ("R", "Não autorizado"),
                ],
                default="S",
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="solicitacao",
            name="status",
            field=models.CharField(
                choices=[
                    ("S", "Solicitado"),
                    ("A", "Autorizado"),
                    ("R", "Não autorizado"),
                    ("C", "Concluído"),
                ],
                default="S",
                max_length=1,
                verbose_name="Status",
            ),
        ),
    ]
