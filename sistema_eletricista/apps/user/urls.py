from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout_then_login
from .views import RegistrarEletricistaView
from .views import QuestionarioView

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^login/$', login, {'template_name':'loginEletricista_exemplo.html', 'redirect_field_name': 'login'}, name='login'),
	url(r'^logout/$', logout_then_login, {'login_url':'/user/login/'}, name='logout'),
	url(r'^index/$', views.index, name='index'),
	url(r'^registrar/$', RegistrarEletricistaView.as_view(), name="registrar"),
	url(r'^questionario/(?P<nome_eletricista>\w+)/$', QuestionarioView.as_view(), name='questionario'),
	url(r'^adm/$', views.adm, name='adm'),
	url(r'^adm/detalhes/(?P<nome_eletricista>\w+)/$', views.detalhes, name='detalhes'),
	url(r'^adm/questionarios_pendentes$', views.questionarios_pendentes, name='questionarios_pendentes'),
	url(r'^adm/aceitar/(?P<nickname>\w+)/$', views.aceitar, name='aceitar'),
	url(r'^adm/recusar/(?P<nickname>\w+)/$', views.recusar, name='recusar'),
]