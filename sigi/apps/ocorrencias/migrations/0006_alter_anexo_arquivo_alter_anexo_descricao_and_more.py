# Generated by Django 4.0.1 on 2022-01-21 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocorrencias', '0005_auto_20210611_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anexo',
            name='arquivo',
            field=models.FileField(max_length=500, upload_to='apps/ocorrencia/anexo/arquivo', verbose_name='Arquivo anexado'),
        ),
        migrations.AlterField(
            model_name='anexo',
            name='descricao',
            field=models.CharField(max_length=70, verbose_name='descrição do anexo'),
        ),
        migrations.AlterField(
            model_name='anexo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tipocontato',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
