# Generated by Django 4.2.4 on 2023-09-28 11:57

from django.db import migrations


def forwards(apps, schema_editor):
    Evento = apps.get_model("eventos", "Evento")

    Evento.objects.all().update(
        publicar=False,
        contato_inscricao="Central de Atendimento - Oficinas.",
        observacao_inscricao=(
            "Passo a passo para a inscrição:<BR>"
            "1. Acesse a plataforma Saberes para ir direto ao curso.<BR>"
            "2. Para efetivar a matrícula, insira a CHAVE DE INSCRIÇÃO "
            "indicada acima.<BR>"
            "3. Dentro da plataforma Saberes, preencha o PERFIL DO ESTUDANTE "
            "e junte-se ao grupo do Whatsapp para receber informações.<BR>"
            "4. No dia da Oficina, leve seu notebook com mouse, "
            "se possível.<BR>"
            "ATENÇÃO: as inscrições ficarão abertas até o dia anterior ao "
            "início da Oficina (14h), ou até atingir o número máximo "
            "de participantes."
        ),
        telefone_inscricao="(61)3303-2026 ; (61)99862-7973 (zap)",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("eventos", "0047_alter_evento_contato_inscricao_and_more"),
    ]

    operations = [migrations.RunPython(forwards)]
