from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout_then_login
from .views import RegistrarEletricistaView
from .views import QuestionarioView
from .views import *
from . import views
from sistema_eletricista.apps.user.eletricista.views import *


urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^login/$', login, {'template_name':'loginEletricista_exemplo.html', 'redirect_field_name': 'login'}, name='login'),
	url(r'^logout/$', logout_then_login, {'login_url':'/user/login/'}, name='logout'),
	url(r'^index/$', views.index, name='index'),
	url(r'^registrar/$', RegistrarEletricistaView.as_view(), name="registrar"),
	url(r'^questionario/(?P<nome_eletricista>\w+)/$', QuestionarioView.as_view(), name='questionario'),
	url(r'^adm/$', views.adm, name='adm'),
	url(r'^adm/questionarios_pendentes$', views.questionarios_pendentes, name='questionarios_pendentes'),
	url(r'^adm/aceitar/(?P<nickname>\w+)/$', views.aceitar, name='aceitar'),
	url(r'^adm/recusar/(?P<nickname>\w+)/$', views.recusar, name='recusar'),
	url(r'^adm/perfil_eletricista/(?P<nickname>\w+)/$', views.perfil_eletricista, name='perfil_eletricista'),
	url(r'^adm/perfil_cliente/(?P<nickname>\w+)/$', views.perfil_cliente, name='perfil_cliente'),
	url(r'^adm/eletricistas_registrados/$', views.eletricistas_registrados, name='eletricistas_registrados'),
	url(r'^adm/bloquear_eletricista/(?P<nickname>\w+)/$', views.bloquear_eletricista_registrado, name='bloquear_eletricista_registrado'),
	url(r'^adm/desbloquear_eletricista/(?P<nickname>\w+)/$', views.desbloquear_eletricista_registrado, name='desbloquear_eletricista_registrado'),
	url(r'^registrar_adm/$', RegistrarAdministradorView.as_view(), name="registraradm"),
    url(r'^buscar-eletricista/$', views.BuscaEletricista, name='BuscaEletricista'),
   	url(r'^adm/clientes_registrados/$', views.clientes_registrados, name='clientes_registrados'),
   	url(r'^buscar-cliente/$', views.BuscaCliente, name='BuscaCliente'),
]