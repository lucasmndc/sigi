# Generated by Django 4.0.4 on 2022-05-29 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0005_remove_coligacao_legislatura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='sigla',
            field=models.CharField(max_length=20, verbose_name='sigla'),
        ),
    ]
