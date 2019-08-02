from django.urls import path

from . import views
from views import *
from sistema_eletricista.apps.user.eletricista.views import *


url(r'^buscar-eletricista/$', views.BuscaEletricista, name='BuscaEletricista'),
