from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import views as auth_views
from .views import RegistrarEletricistaView
from .views import QuestionarioView
from .views import *
from . import views
from sistema_eletricista.apps.user.eletricista.views import *
from sistema_eletricista.apps.user.cliente.views import *
from sistema_eletricista.apps.user.views import *

urlpatterns = [
	url(r'^servico/(?P<id_servico>\w+)/$', views.servico_ws , name="servico_ws"),
	url(r'^cliente/$', views.tela_cliente, name='tela_cliente'),
	url(r'^index/$', views.index, name='index'),
	url(r'^index/historico-de-servicos', views.ListarPedidos, name='ListarPedidos'),
	url(r'^index/pagamento', views.Pagamento, name='Pagamento'),
	url(r'^index/perfil/(?P<nickname>\w+)/$', Perfil_do_cliente.as_view(), name='Perfil_do_cliente'),
	url(r'^eletricista/$', views.tela_eletricista, name='tela_eletricista'),
	url(r'^admin/', admin.site.urls),
	url(r'^login/$', login, {'template_name':'loginEletricista_exemplo.html', 'redirect_field_name': 'login'}, name='login'),
	url(r'^logout/$', logout_then_login, {'login_url':'/user/login/'}, name='logout'),
	url(r'^registrar/$', RegistrarEletricistaView.as_view(), name="registrar"),
	url(r'^registrar/cartao/(?P<nickname_cliente>\w+)/', RegistrarCartaoView.as_view(), name="registrar_cartao"),
	url(r'^registrar/conta/(?P<user_pk>\w+)', RegistrarRecebedorView.as_view(), name="registrar_recebedor"),
	url(r'^password_reset/$', auth_views.password_reset, {'template_name':'password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,{'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,{'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,{'template_name':'password_reset_complete.html'}, name='password_reset_complete'),
	url(r'^questionario/(?P<nome_eletricista>\w+)/$', QuestionarioView.as_view(), name='questionario'),
	url(r'^registro_concluido/$', views.registro_concluido, name='registro_concluido'),
	url(r'^adm/$', views.adm, name='adm'),
	url(r'^index/alterar-senha/$', views.change_password, name='change_password'),
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
   	url(r'^registrar_cliente/$', RegistrarEletricistaView.as_view(), name='registrar_cliente'),
   	url(r'^registrar_eletricista/$', RegistrarEletricistaView.as_view(), name='registrar_eletricista'),
   	url(r'^base/$', views.Base, name='base'),
   	url(r'^dump/$', views.dump, name='dump'),
   	url(r'^servico/$', views.servico, name='servico'),
   	url(r'^servico_avaliar/$', views.servico_avaliar, name='servico_avaliar'),
   	url(r'^avaliar/$', views.avaliar, name='avaliar'),
<<<<<<< HEAD
   	url(r'^tela1/(?P<id_servico>\w+)/(?P<valor_servico>\w+)$', Tela1.as_view(), name='tela1'),
   	url(r'^tela2/(?P<id_servico>\w+)$', Tela2.as_view(), name='tela2'),
=======
   	url(r'^tela1/$', Tela1.as_view(), name='tela1'),
   	url(r'^tela2/$', Tela2.as_view(), name='tela2'),
   	url(r'^escolhe_cadastro/$', Escolhe_Cadastro.as_view(), name='escolhe_cadastro'),
>>>>>>> 63a71923f756ffc610d0aeb89cf481501b3f41d4

]
