from django.urls import path

from . import views
from views import Cliente
from sistema_eletricista.apps.user.cliente.views import Cliente


url(r'^buscar-cliente/$', views.BuscaEletricista, name='BuscaCliente'),

