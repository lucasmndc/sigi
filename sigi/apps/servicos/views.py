import csv
from django.db.models import Q, Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import ListView
from import_export import resources
from import_export.fields import Field
from sigi.apps.casas.models import Orgao
from sigi.apps.contatos.models import UnidadeFederativa
from sigi.apps.eventos.models import Evento
from sigi.apps.servicos.models import Servico
from sigi.apps.utils import to_ascii


class ServicoResource(resources.ModelResource):
    telefone = Field(column_name="casa_legislativa__telefone")

    class Meta:
        model = Servico
        fields = [
            "casa_legislativa__cnpj",
            "casa_legislativa__nome",
            "casa_legislativa__tipo__nome",
            "casa_legislativa__logradouro",
            "casa_legislativa__bairro",
            "casa_legislativa__cep",
            "casa_legislativa__municipio__nome",
            "casa_legislativa__municipio__uf__sigla",
            "casa_legislativa__email",
            "telefone",
            "tipo_servico__nome",
            "data_ativacao",
            "url",
        ]
        export_order = fields

        def dehydrate_telefone(self, servico):
            return servico.casa_legislativa.telefone


class CasasAtendidasListView(ListView):
    model = Servico
    template_name = "servicos/casas_atendidas.html"
    paginate_by = 100

    def get_queryset(self):
        param = self.kwargs["param"]
        search_param = self.request.GET.get("search", None)

        oficinas_qs = (
            Evento.objects.exclude(data_inicio=None)
            .exclude(data_termino=None)
            .filter(status=Evento.STATUS_REALIZADO)
        )

        queryset = super().get_queryset()
        queryset = (
            queryset.filter(
                data_desativacao=None, casa_legislativa__tipo__legislativo=True
            )
            .select_related(
                "tipo_servico",
                "casa_legislativa",
                "casa_legislativa__municipio",
                "casa_legislativa__municipio__uf",
                "casa_legislativa__tipo",
            )
            .prefetch_related(
                "casa_legislativa__convenio_set",
                Prefetch(
                    "casa_legislativa__evento_set",
                    oficinas_qs,
                    to_attr="oficinas",
                ),
            )
            .order_by(
                "casa_legislativa__municipio__uf__nome",
                "casa_legislativa__tipo__nome",
                "casa_legislativa__nome",
                "tipo_servico__nome",
            )
        )
        if search_param:
            filter = [
                Q(casa_legislativa__search_text__icontains=to_ascii(t.lower()))
                for t in search_param.split()
            ]
            queryset = queryset.filter(*filter)
        if param.isdigit():
            queryset = queryset.filter(casa_legislativa__id=param)
        elif param != "_all_":
            queryset = queryset.filter(
                casa_legislativa__municipio__uf__sigla=param
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        param = self.kwargs["param"]
        context["tot_orgaos"] = (
            self.get_queryset()
            .order_by()
            .distinct("casa_legislativa__id")
            .count()
        )
        context["regioes"] = [
            (
                regiao,
                UnidadeFederativa.objects.filter(regiao=r).exclude(sigla="ZZ"),
            )
            for r, regiao in UnidadeFederativa.REGIAO_CHOICES
        ]
        context["search_param"] = self.request.GET.get("search", None)
        if param != "_all_" and not param.isdigit():
            context["uf"] = UnidadeFederativa.objects.get(sigla=param)
        return context

    def render_to_response(self, context, **response_kwargs):
        format = self.request.GET.get("format", "html")
        if format == "csv":
            servicos = self.get_queryset()
            data = ServicoResource().export(servicos)
            return HttpResponse(
                data.csv,
                content_type="text/csv",
                headers={
                    "Content-Disposition": 'attachment;filename="orgaos_interlegis.csv"'
                },
            )
        return super().render_to_response(context, **response_kwargs)

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
