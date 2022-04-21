# Generated by Django 4.0.1 on 2022-01-12 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("convenios", "0018_auto_20211208_1256"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anexo",
            name="arquivo",
            field=models.FileField(
                max_length=500, upload_to="apps/convenios/anexo/arquivo"
            ),
        ),
        migrations.AlterField(
            model_name="anexo",
            name="descricao",
            field=models.CharField(max_length=70, verbose_name="descrição"),
        ),
        migrations.AlterField(
            model_name="anexo",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="convenio",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="convenio",
            name="id_contrato_gescon",
            field=models.CharField(
                blank=True,
                default="",
                editable=False,
                max_length=20,
                verbose_name="ID do contrato no Gescon",
            ),
        ),
        migrations.AlterField(
            model_name="equipamentoprevisto",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="gescon",
            name="email",
            field=models.EmailField(
                help_text="Caixa de e-mail para onde o relatório diário de importação será enviado.",
                max_length=254,
                verbose_name="E-mail",
            ),
        ),
        migrations.AlterField(
            model_name="gescon",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="projeto",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="statusconvenio",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="tiposolicitacao",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="tramitacao",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="tramitacao",
            name="observacao",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="observação"
            ),
        ),
        migrations.AlterField(
            model_name="unidadeadministrativa",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="unidadeadministrativa",
            name="nome",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="unidadeadministrativa",
            name="sigla",
            field=models.CharField(max_length=10),
        ),
    ]
