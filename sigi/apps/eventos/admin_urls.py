from django.urls import path, include
from sigi.apps.eventos import views

urlpatterns = [
    path("calendario/", views.calendario, name="eventos_calendario"),
    path(
        "alocacaoequipe/", views.alocacao_equipe, name="eventos_alocacaoequipe"
    ),
    path("eventosporuf/", views.eventos_por_uf, name="eventos_eventosporuf"),
]
