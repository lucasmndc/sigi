# Generated by Django 4.0.4 on 2022-04-25 19:45

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('convenios', '0020_gescon_orgaos_gestores'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='texto_minuta',
            field=tinymce.models.HTMLField(blank=True, help_text='Use as seguintes marcações:<ul><li>{{ casa.nome }} para o nome da Casa Legislativa / órgão</li><li>{{ casa.municipio.uf.sigla }} para a sigla da UF da Casa legislativa</li><li>{{ presidente.nome }} para o nome do presidente</li><li>{{ contato.nome }} para o nome do contato Interlegis</li></ul>', verbose_name='texto da minuta'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='texto_oficio',
            field=tinymce.models.HTMLField(blank=True, help_text='Use as seguintes marcações:<ul><li>{{ casa.nome }} para o nome da Casa Legislativa / órgão</li><li>{{ casa.municipio.uf.sigla }} para a sigla da UF da Casa legislativa</li><li>{{ presidente.nome }} para o nome do presidente</li><li>{{ contato.nome }} para o nome do contato Interlegis</li></ul>', verbose_name='texto do ofício'),
        ),
    ]
