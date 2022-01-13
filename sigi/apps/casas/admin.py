from unicodedata import name
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from import_export import resources
from import_export.fields import Field
from sigi.apps.casas.forms import OrgaoForm
from sigi.apps.casas.models import Orgao, Presidente, Funcionario, TipoOrgao
# from sigi.apps.casas.views import report_complete, labels_report, export_csv, \
#     labels_report_sem_presidente, report, \
#     adicionar_casas_carrinho
from sigi.apps.casas.filters import (GerentesInterlegisFilter, ConvenioFilter,
                                     ExcluirConvenioFilter)
from sigi.apps.contatos.models import Telefone
from sigi.apps.convenios.models import Convenio, Projeto
# from sigi.apps.ocorrencias.models import Ocorrencia
# from sigi.apps.servicos.models import Servico, TipoServico
from sigi.apps.utils import queryset_ascii
from sigi.apps.utils.mixins import CartExportMixin


class OrgaoExportResourse(resources.ModelResource):
    presidente = Field(column_name='presidente')
    telefone = Field(column_name='telefone')
    num_parlamentares = Field(column_name='num_parlamentares')
    # servicos_seit = Field(column_name='servicos_seit')
    contato = Field(column_name='contato')
    class Meta:
        model = Orgao
        fields = ('municipio__codigo_ibge', 'cnpj', 'municipio__codigo_tse',
                  'nome', 'municipio__nome', 'municipio__uf__sigla',
                  'presidente', 'logradouro', 'bairro', 'cep', 'telefone',
                  'pagina_web', 'email', 'telefone', 'num_parlamentares',
                  'ult_alt_endereco', 'contato')
        export_order = fields

    def dehydrate_presidente(self, orgao):
        return orgao.presidente

    def dehydrate_telefone(self, orgao):
        return orgao.telefone

    def dehydrate_num_parlamentares(self, orgao):
        return orgao.num_parlamentares

    # def dehydrate_servicos_seit(self, orgao):
    #     servicos = [s.tipo_servico.nome for s in orgao.servico_set.filter(
    #         data_desativacao__isnull=True)]
    #     return ", ".join(servicos)

    def dehydrate_contato(self, orgao):
        return ", ".join(
            [f"{c.cargo if c.cargo else 'Sem cargo'}: {c.nome} ({c.email})"
             for c in orgao.funcionario_set.filter(desativado=False)
            ]
        )

class TelefonesInline(GenericTabularInline):
    model = Telefone
    readonly_fields = ('ult_alteracao',)
    extra = 1

class PresidenteInline(admin.StackedInline):
    model = Presidente
    fields = ('nome', 'sexo', 'data_nascimento', 'nota', 'email',
              'tempo_de_servico', 'ult_alteracao', 'endereco', 'municipio',
              'bairro', 'cep', 'redes_sociais',)
    raw_id_fields = ('municipio',)
    readonly_fields = ('ult_alteracao',)
    extra = 1
    max_num = 1
    verbose_name_plural = _('Presidente')
    def get_queryset(self, request):
        return (self.model.objects.exclude(desativado=True)
        .extra(select={'ult_null': 'ult_alteracao is null'})
        .order_by('ult_null', '-ult_alteracao')
            # A função extra foi usada para quando existir um registro com o
            # campo igual a null não aparecer na frente dos mais novos
        )

class ContatoInterlegisInline(admin.StackedInline):
    model = Funcionario
    fields = ('nome', 'sexo', 'data_nascimento', 'nota', 'email', 'cargo',
              'funcao', 'setor', 'tempo_de_servico', 'ult_alteracao',
              'endereco', 'municipio', 'bairro', 'cep', 'redes_sociais',
              'desativado', 'observacoes')
    raw_id_fields = ('municipio',)
    readonly_fields = ('ult_alteracao',)
    extra = 1
    inlines = (TelefonesInline,)
    verbose_name_plural = _('Contato(s) Interlegis Vigente(s)')
    def get_queryset(self, request):
        return (self.model.objects.filter(setor='contato_interlegis')
        .extra(select={'ult_null': 'ult_alteracao is null'}).order_by(
            '-ult_alteracao')
        )
    def get_extra(self, request, obj=None , **kwargs):
        extra = 0
        return extra

class FuncionariosInline(admin.StackedInline):
    model = Funcionario
    fields = ('nome', 'sexo', 'data_nascimento', 'nota', 'email', 'cargo',
              'funcao', 'setor', 'tempo_de_servico', 'ult_alteracao',
              'endereco', 'municipio', 'bairro', 'cep', 'redes_sociais',
              'desativado', 'observacoes')
    raw_id_fields = ('municipio',)
    readonly_fields = ('ult_alteracao',)
    extra = 1
    inlines = (TelefonesInline,)
    verbose_name_plural = _('Outros Contatos da Casa')

    def get_queryset(self, request):
        return (self.model.objects.exclude(cargo='Presidente',)
        .exclude(desativado=True).extra(
            select={'ult_null': 'ult_alteracao is null'})
        .order_by('ult_null', '-ult_alteracao')
            # A função extra foi usada para quando existir um registro com
            # o campo igual a null não aparecer na frente dos mais novos
        )

class ConveniosInline(admin.TabularInline):
    model = Convenio
    fieldsets = (
        (None, {'fields': (
            ('link_sigad', 'status_convenio', 'num_convenio',
             'projeto', 'observacao'),
            ('data_retorno_assinatura', 'data_pub_diario',),
            ('get_anexos',),
            ('link_convenio',),
        )}),
    )
    readonly_fields = ['link_convenio', 'link_sigad', 'status_convenio',
                       'num_convenio', 'projeto', 'observacao', 'data_adesao',
                       'data_retorno_assinatura', 'data_termo_aceite',
                       'data_pub_diario', 'data_devolucao_via',
                       'data_postagem_correio', 'data_devolucao_sem_assinatura',
                       'data_retorno_sem_assinatura', 'get_anexos']
    extra = 0
    can_delete = False
    template = 'admin/casas/convenios_inline.html'
    ordering = ('-data_retorno_assinatura',)

    def has_add_permission(self, request):
        return False

    def get_anexos(self, obj):
        return mark_safe('<br/>'.join(
            [f'<a href="{a.arquivo.url}" target="_blank">{a}</a>'
             for a in obj.anexo_set.all()])
        )
    get_anexos.short_description = _('Anexos')

    def status_convenio(self, obj):
        if obj.pk is None:
            return ""
        status = obj.get_status()

        if status in ["Vencido", "Desistência", "Cancelado"]:
            label = r"danger"
        elif status == "Vigente":
            label = r"success"
        elif status == "Pendente":
            label = r"warning"
        else:
            label = r"info"

        return mark_safe(f'<p class="label label-{label}">{status}</p>')
    status_convenio.short_description = _("Status do convênio")

    def link_convenio(self, obj):
        if obj.pk is None:
            return ""
        url = reverse(
            f'admin:{obj._meta.app_label}_{obj._meta.module_name}_change',
            args=[obj.pk]
        ) + '?_popup=1'
        return mark_safe(
            f'<input id="edit_convenio-{obj.pk}" type="hidden"/>'
            f'<a id="lookup_edit_convenio-{obj.pk}" href="{url}"'
            'class="changelink" '
            'onclick="return showRelatedObjectLookupPopup(this)">'
            f'{_("Editar")}</a>'
        )
    link_convenio.short_description = _('Editar convenio')

    def link_sigad(self, obj):
        if obj.pk is None:
            return ""
        return mark_safe(obj.get_sigad_url())
    link_sigad.short_description = _("Processo no Senado")

# class ServicoInline(admin.TabularInline):
#     model = Servico
#     fields = ('link_url', 'contato_tecnico', 'contato_administrativo',
#               'hospedagem_interlegis', 'data_ativacao', 'data_alteracao',
#               'data_desativacao', 'link_servico')
#     readonly_fields = ['link_url', 'contato_tecnico', 'contato_administrativo',
#                        'hospedagem_interlegis', 'data_ativacao',
#                        'data_alteracao', 'data_desativacao', 'link_servico']
#     extra = 0
#     max_num = 0
#     can_delete = False
#     ordering = ('-data_alteracao',)

#     def link_url(self, servico):
#         if servico.data_desativacao is not None:
#             return servico.url
#         return mark_safe(
#             f'<a href="{servico.url}" target="_blank">{servico.url}</a>'
#         )
#     link_url.short_description = _('URL do serviço')

#     def link_servico(self, obj):
#         if obj.pk is None:
#             return ""
#         url = reverse(
#             f'admin:{obj._meta.app_label}_{obj._meta.module_name_change}',
#             args=[obj.pk]
#         ) + '?_popup=1'
#         return mark_safe(
#             f'<input id="edit_convenio-{obj.pk}" type="hidden"/>'
#             f'<a id="lookup_edit_convenio-{obj.pk}" href="{url}" '
#             'class="changelink" '
#             'onclick="return showRelatedObjectLookupPopup(this)">Editar</a>'
#         )
#     link_servico.short_description = _('Editar Serviço')

#     def has_add_permission(self, request):
#         return False

# class OcorrenciaInline(admin.TabularInline):
#     model = Ocorrencia
#     fields = ('data_criacao', 'assunto', 'prioridade', 'status',
#               'data_modificacao', 'setor_responsavel', 'link_editar',)
#     readonly_fields = ('data_criacao', 'assunto', 'prioridade', 'status',
#                        'data_modificacao', 'setor_responsavel', 'link_editar',)
#     extra = 0
#     max_num = 0
#     can_delete = False
#     template = 'admin/casas/ocorrencia_inline.html'
#     ordering = ('-data_modificacao',)

#     def link_editar(self, obj):
#         if obj.pk is None:
#             return ""
#         url = reverse(
#             f'admin:{obj._meta.app_label}_{obj._meta.module_name}_change',
#             args=[obj.pk]
#         )
#         return mark_safe(
#             f'<input id="edit_ocorrencia-{obj.pk}" type="hidden"/>'
#             f'<a id="lookup_edit_ocorrencia-{obj.pk}" href="{url}" '
#             'class="button" target="_blank" '
#             'onclick="return showRelatedObjectLookupPopup(this);">'
#             f'{_("Editar")}</a>'
#         )
#     link_editar.short_description = _('Editar')


@admin.register(Orgao)
class OrgaoAdmin(CartExportMixin, admin.ModelAdmin):
    form = OrgaoForm
    resource_class = OrgaoExportResourse
    # actions = ['adicionar_casas', ]
    inlines = (TelefonesInline, PresidenteInline, ContatoInterlegisInline,
               FuncionariosInline, ) #ConveniosInline, ServicoInline,
            #    OcorrenciaInline,)
    list_display = ('id', 'sigla', 'nome', 'get_uf', 'get_gerentes',
                    'get_convenios', 'get_servicos')
    list_display_links = ('sigla', 'nome',)
    # list_filter = ('tipo', ('gerentes_interlegis', GerentesInterlegisFilter),
    #                'municipio__uf__nome', ConvenioFilter, ServicoAtivoFilter,
    #                ExcluirConvenioFilter, ServicoFilter, 'inclusao_digital',)
    list_filter = ('tipo', ('gerentes_interlegis', GerentesInterlegisFilter),
                   'municipio__uf__nome', ConvenioFilter, ExcluirConvenioFilter,
                   'inclusao_digital',)
    ordering = ('municipio__uf__nome', 'nome')
    queryset = queryset_ascii
    fieldsets = (
        (None, {
            'fields': ('tipo', 'nome', 'sigla', 'cnpj', 'num_parlamentares',
                       'gerentes_interlegis')
        }),
        (_('Endereço'), {
            'fields': ('data_instalacao', 'logradouro', 'bairro',
                       'municipio', 'cep', 'ult_alt_endereco'),
        }),
        (_('Presença na Internet'), {
            'fields': ('inclusao_digital', 'data_levantamento', 'pesquisador',
                       'pagina_web', 'email', 'obs_pesquisa',)
        }),
        (_('Outras informações'), {
            'fields': ('observacoes', 'horario_funcionamento', 'foto',
                       'recorte'),
        }),
    )
    raw_id_fields = ('municipio',)
    readonly_fields = ['num_parlamentares', 'gerentes_interlegis',]
    search_fields = ('search_text', 'sigla', 'cnpj', 'bairro', 'logradouro',
                     'cep', 'municipio__nome', 'municipio__uf__nome',
                     'municipio__codigo_ibge', 'pagina_web', 'observacoes')

    def get_uf(self, obj):
        return obj.municipio.uf.nome
    get_uf.short_description = _('Unidade da Federação')
    get_uf.admin_order_field = 'municipio__uf__nome'

    def get_gerentes(self, obj):
        return mark_safe(obj.lista_gerentes())
    get_gerentes.short_description = _('Gerente Interlegis')

    def get_convenios(self, obj):
        return mark_safe(
            '<ul>' +
            ''.join([f'<li>{c}</li>' for c in obj.convenio_set.all()]) +
            '</ul>'
        )
    get_convenios.short_description = _('Convênios')

    def get_servicos(self, obj):
        #TODO: Descomentar após migrar a app Servicos
        # return mark_safe(
        #     '<ul>' +
        #     ''.join(
        #         [f'<li><a href="{s.url}" target="_blank">{s}</a></li>'
        #          for s in obj.servico_set.filter(
        #              data_desativacao__isnull=True)
        #         ]
        #     ) +
        #     '</ul>'
        # )
        return "TODO: Descomentar após migrar a app Servicos"
    get_servicos.short_description = _('Serviços')

    def changelist_view(self, request, extra_context=None):
        return super(OrgaoAdmin, self).changelist_view(
            request,
            extra_context={'query_str': '?' + request.META['QUERY_STRING']}
        )

    def lookup_allowed(self, lookup, value):
        return (super(OrgaoAdmin, self).lookup_allowed(lookup, value) or
                lookup in ['tipo__legislativo__exact',
                           'tipo__sigla__exact',
                           'municipio__uf__codigo_ibge__exact',
                           'convenio__projeto__id__exact'])

    #TODO: Resolver depois - sigi-boys???
    # def etiqueta(self, request, queryset):
    #     return labels_report(request, queryset=queryset)
    # etiqueta.short_description = _("Gerar etiqueta(s) da(s) casa(s) "
    #                                "selecionada(s)")

    # def etiqueta_sem_presidente(self, request, queryset):
    #     return labels_report_sem_presidente(request, queryset=queryset)
    # etiqueta_sem_presidente.short_description = _("Gerar etiqueta(s) sem "
    #                                               "presidente da(s) casa(s) "
    #                                               "selecionada(s)")

    # def relatorio(self, request, queryset):
    #     return report(request, queryset=queryset)
    # relatorio.short_description = _("Exportar a(s) casa(s) selecionada(s) "
    #                                 "para PDF")

    # def relatorio_completo(self, request, queryset):
    #     return report_complete(request, queryset=queryset)
    # relatorio_completo.short_description = _("Gerar relatório completo da(s) "
    #                                          "casa(s) selecionada(s)")

    # def relatorio_csv(self, request, queryset):
    #     return export_csv(request)
    # relatorio_csv.short_description = _("Exportar casa(s) selecionada(s) "
    #                                     "para CSV")

    # def adicionar_casas(self, request, queryset):
    #     if 'carrinho_casas' in request.session:
    #         # if request.session.has_key('carrinho_casas'):
    #         q1 = len(request.session['carrinho_casas'])
    #     else:
    #         q1 = 0
    #     response = adicionar_casas_carrinho(request, queryset=queryset)
    #     q2 = len(request.session['carrinho_casas'])
    #     quant = q2 - q1
    #     if quant:
    #         self.message_user(request, str(q2 - q1) + " " +
    #                           _("Casas Legislativas adicionadas no carrinho"))
    #     else:
    #         self.message_user(request, _("As Casas Legislativas selecionadas "
    #                                      "já foram adicionadas anteriormente"))
    #     return HttpResponseRedirect('.')

    # adicionar_casas.short_description = _("Armazenar casas no carrinho para "
    #                                       "exportar")

    def get_actions(self, request):
        actions = super(OrgaoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions