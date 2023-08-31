# Generated by Django 4.2.4 on 2023-08-30 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("servidores", "0013_servidor_moodle_userid"),
        ("casas", "0027_alter_orgao_email"),
        ("eventos", "0036_tipoevento_prefixo_turma_alter_evento_turma"),
    ]

    operations = [
        migrations.AddField(
            model_name="tipoevento",
            name="duracao",
            field=models.PositiveIntegerField(
                default=1, verbose_name="Duração (dias)"
            ),
        ),
        migrations.AddField(
            model_name="tipoevento",
            name="sigla",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="sigla"
            ),
        ),
        migrations.CreateModel(
            name="Solicitacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "senador",
                    models.CharField(
                        max_length=100, verbose_name="senador solicitante"
                    ),
                ),
                (
                    "num_processo",
                    models.CharField(
                        blank=True,
                        help_text="Formato:<em>XXXXX.XXXXXX/XXXX-XX</em>",
                        max_length=20,
                        verbose_name="número do processo SIGAD",
                    ),
                ),
                (
                    "descricao",
                    models.TextField(verbose_name="descrição da solicitação"),
                ),
                (
                    "data_pedido",
                    models.DateField(
                        help_text="Data em que o pedido do Gabinete chegou à COPERI",
                        verbose_name="Data do pedido",
                    ),
                ),
                (
                    "contato",
                    models.CharField(
                        max_length=100,
                        verbose_name="pessoa de contato na Casa",
                    ),
                ),
                (
                    "email_contato",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="e-mail do contato",
                    ),
                ),
                (
                    "telefone_contato",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        verbose_name="telefone do contato",
                    ),
                ),
                (
                    "whatsapp_contato",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        verbose_name="whatsapp do contato",
                    ),
                ),
                (
                    "estimativa_casas",
                    models.PositiveIntegerField(
                        help_text="estimativa de quantas Casas participarão dos eventos",
                        verbose_name="estimativa de Casas participantes",
                    ),
                ),
                (
                    "estimativa_servidores",
                    models.PositiveIntegerField(
                        help_text="estimativa de quantos Servidores participarão dos eventos",
                        verbose_name="estimativa de servidores participantes",
                    ),
                ),
                (
                    "casa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="casas.orgao",
                        verbose_name="casa solicitante",
                    ),
                ),
            ],
            options={
                "verbose_name": "Solicitação de eventos",
                "verbose_name_plural": "Solicitações de eventos",
                "ordering": ("-data_pedido",),
            },
        ),
        migrations.CreateModel(
            name="ItemSolicitado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "virtual",
                    models.BooleanField(default=False, verbose_name="virtual"),
                ),
                (
                    "inicio_desejado",
                    models.DateField(
                        help_text="Data desejada para o início do evento. Pode ser solicitado pela Casa ou definido pela conveniência do Interlegis. Será usada como data de início do evento, caso seja autorizado.",
                        verbose_name="início desejado",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("S", "Solicitado"),
                            ("A", "Autorizado"),
                            ("R", "Rejeitado"),
                        ],
                        default="S",
                        verbose_name="status",
                    ),
                ),
                (
                    "data_analise",
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="data da autorização/rejeição",
                    ),
                ),
                (
                    "justificativa",
                    models.TextField(blank=True, verbose_name="Justificativa"),
                ),
                (
                    "evento",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="eventos.evento",
                    ),
                ),
                (
                    "servidor",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        help_text="Servidor que autorizou ou rejeitou a realização do evento",
                        limit_choices_to={"externo": False},
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="servidores.servidor",
                        verbose_name="servidor analisador",
                    ),
                ),
                (
                    "solicitacao",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eventos.solicitacao",
                    ),
                ),
                (
                    "tipo_evento",
                    models.ForeignKey(
                        limit_choices_to={"casa_solicita": True},
                        on_delete=django.db.models.deletion.PROTECT,
                        to="eventos.tipoevento",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evento solicitado",
                "verbose_name_plural": "Eventos solicitados",
                "ordering": ("status",),
            },
        ),
    ]
