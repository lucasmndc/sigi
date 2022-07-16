# Generated by Django 4.0.4 on 2022-05-16 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0011_remove_servico_contato_administrativo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='data_verificacao',
            field=models.DateTimeField(blank=True, null=True, verbose_name='data da última verificação'),
        ),
        migrations.AddField(
            model_name='servico',
            name='resultado_verificacao',
            field=models.CharField(choices=[('N', 'Não verificado'), ('F', 'Funcionando'), ('U', 'Nunca foi usado'), ('D', 'Acesso negado'), ('O', 'Fora do ar'), ('I', 'Dados imcompatíveis - não é serviço Interlegis')], default='N', max_length=1, verbose_name='resultado da verificação'),
        ),
    ]