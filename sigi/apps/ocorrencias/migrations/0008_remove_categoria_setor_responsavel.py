# Generated by Django 4.0.1 on 2022-02-13 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ocorrencias", "0007_remove_comentario_encaminhar_setor_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categoria",
            name="setor_responsavel",
        ),
    ]
