# Generated by Django 4.0.3 on 2022-04-20 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eventos", "0018_evento_data_pedido_evento_num_processo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evento",
            name="status",
            field=models.CharField(
                choices=[
                    ("E", "Em planejamento"),
                    ("G", "Aguardando abertura SIGAD"),
                    ("P", "Previsão"),
                    ("A", "A confirmar"),
                    ("O", "Confirmado"),
                    ("R", "Realizado"),
                    ("C", "Cancelado"),
                    ("Q", "Arquivado"),
                ],
                max_length=1,
                verbose_name="Status",
            ),
        ),
    ]
