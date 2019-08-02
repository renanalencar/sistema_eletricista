#Import from Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
#from vanilla import ListView


#Import from apps
from .forms import RegistrarEletricistaForm
from .forms import RegistrarCartaoForm
from .forms import RegistrarAdministradorForm
from .forms import RegistrarRecebedorForm
from .models import ValorPorHora

#from .forms import QuestionarioForm
from sistema_eletricista.apps.post.PedidoDeServico.models import PedidoDeServico
from .forms import QuestionarioForm
from .eletricista.models import *
from .cliente.models import Cliente
from .models import Admin
from .models import Coordenadas
from django.contrib.auth.views import *
import pagarme, json
# Create your views here.


#Função de enviar emails
class MudarValorPorHora(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            valores_por_hora = ValorPorHora.objects.all()[0]
        except:
            valores_por_hora = ValorPorHora.objects.create(valor_meia_hora=1, valor_primeira_hora=1, valor_demais_horas=1)



        valores_porhora = ValorPorHora.objects.all()[0]
        meia_hora = request.POST['meia_hora']
        primeira_hora = request.POST['primeira_hora']
        demais_horas = request.POST['demais_horas']

        valores_por_hora.valor_meia_hora = int(meia_hora)
        valores_por_hora.valor_primeira_hora = int(primeira_hora)
        valores_por_hora.valor_demais_horas = int(demais_horas)

        valores_por_hora.save()
        return render(request, 'dashboard_exemplo.html')


@login_required(login_url='/user/login/')
def servico_ws(request, id_servico):
    return render(request, 'servico_ws.html', {'nome' : get_usuario_logado(request),
                                                'ip' : get_client_ip(request),
                                                'user': request.user,
                                            })

def usuario_e_eletricista(user):
    usuario_em_questao = User.objects.get(username=user)
    e_eletricista = Eletricista.objects.filter(usuario=usuario_em_questao)
    if e_eletricista:
        return True
    else:
        return False

def usuario_e_cliente(user):
    usuario_em_questao = User.objects.get(username=user)
    e_cliente = Cliente.objects.filter(usuario=usuario_em_questao)
    if e_cliente:
        return True
    else:
        return False


def enviar_email(subject, message, email_from, recipient_list):
    send_mail(subject, message, email_from, recipient_list)
    return;

@login_required(login_url='/user/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('change_password')
        else:
            messages.error(request, 'Não foi possível alterar sua senha.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def get_usuario_logado(request):
    usuario = request.user
    return usuario.first_name

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url='/user/login/')
def index(request):
    
    if request.method == 'GET':
        username = request.user
        usuario = User.objects.get(username=username)
        # userteste = User.objects.get(username='UserCliente')
        
        eletricista_existe = Eletricista.objects.filter(usuario=usuario).exists()
        cliente_existe = Cliente.objects.filter(usuario=usuario).exists()
        admin_existe = Admin.objects.filter(user=usuario).exists()
        if eletricista_existe:
            response =  render(request, 'solicitar_servico.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user,
                'foto' : Eletricista.objects.get(usuario=username).foto
                })
            response.set_cookie('currentstate', True)
            return response
        if cliente_existe:
            cliente = Cliente.objects.get(usuario=usuario)
            return render(request, 'solicitar_servico.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user,
                'foto' : cliente.foto
                })  
        if admin_existe:
            return render(request, 'dashboard_exemplo.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user,
                'numero' : 10
                })
        response =  render(request, 'solicitar_servico.html', {'nome' : get_usuario_logado(request), 'ip' : get_client_ip(request), 'user': request.user})
        response.set_cookie('currentstate', True)
        return response
        #teste para coords

@login_required(login_url='/user/login/')
def Pagamento(request):
    if request.method == 'GET':
        username = request.user
        usuario = User.objects.get(username=username)
        eletricista_existe = Eletricista.objects.filter(usuario=usuario).exists()
        cliente_existe = Cliente.objects.filter(usuario=usuario).exists()
        admin_existe = Admin.objects.filter(user=usuario).exists()
        if eletricista_existe:
            return render(request, 'pagamento_eletricista.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user
                })
        if cliente_existe:
            return render(request, 'pagamento_cliente.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user
                })  
        if admin_existe:
            return render(request, 'pagamento_admin.html', {
                'nome' : get_usuario_logado(request),
                'ip' : get_client_ip(request),
                'user': request.user
                })
        #return render(request, 'solicitar_servico.html', {'nome' : get_usuario_logado(request), 'ip' : get_client_ip(request), 'user': request.user})

@login_required(login_url='/user/login/')
def BuscaEletricista(request):
    q = request.GET.get('buscaEletricista')
    if q is not None:
        resultEletricista = Eletricista.objects.BuscarEletricista(q)
    return render(request, 'busca_eletricista.html', {'resultEletricista' : resultEletricista})


@login_required(login_url='/user/login/')
def BuscaCliente(request):
    q1 = request.GET.get('buscaCliente')
    if q1 is not None:
        resultCliente = Cliente.objects.BuscarCliente(q1)
    return render(request, 'busca_cliente.html', {'resultCliente': resultCliente})

class RegistrarCartaoView(View):

    template_name = 'registrar_cartao.html'
    def get(self, request, nickname_cliente):
        print ('estou com o nickname')
        print (nickname_cliente)
        return render(request, self.template_name)

    def post(self, request, nickname_cliente):
        form_cartao = RegistrarCartaoForm(request.POST)
        if form_cartao.is_valid():
            dados_form_cartao = form_cartao.data

            pagarme.authentication_key('ak_test_uSXZcO1zJua2nG3ZhjmiUwcwnxnCgM')

            card_data = {
                "card_expiration_date": dados_form_cartao['card_expiration_date'].replace("/", ""),
                "card_number": dados_form_cartao['card_number'].replace(" ", ""),
                "card_cvv": dados_form_cartao['card_cvv'],
                "card_holder_name": dados_form_cartao['card_holder_name'],
                "id_customer": nickname_cliente,

                }

            print (card_data)
            print (pagarme.card.create(card_data))

            return redirect('tela_cliente')
        else:
            return render(request, 'registrar_cartao.html', {'form' : form_cartao})

class RegistrarRecebedorView(View):

    template_name = 'registrar_recebedor.html'
    def get(self, request, user_pk):
        return render(request, self.template_name)

    def post(self, request, user_pk):
        form_recebedor = RegistrarRecebedorForm(request.POST)
        if form_recebedor.is_valid():
            dados_form_recebedor = form_recebedor.data
            user = User.objects.get(pk=user_pk)
            eletricista = Eletricista.objects.get(usuario = user)

            pagarme.authentication_key('ak_test_uSXZcO1zJua2nG3ZhjmiUwcwnxnCgM')

            params = {
                'anticipatable_volume_percentage': '80',
                'automatic_anticipation_enabled': 'true',
                'transfer_day': '5',
                'transfer_enabled': 'true',
                'transfer_interval': 'weekly',
                'bank_account':{
                    'agencia': dados_form_recebedor['agencia'],
                    'agencia_dv': '5',
                    'bank_code': dados_form_recebedor['bank_code'],
                    'conta': dados_form_recebedor['conta'],
                    'conta_dv': "1",
                    'document_number': eletricista.CPF,
                    'legal_name': eletricista.usuario.first_name
                }
            }

            recipient = pagarme.recipient.create(params)
            eletricista.pagarme_id = recipient["id"]
            eletricista.save()

            return HttpResponseRedirect(reverse('questionario', kwargs={'nome_eletricista': user.pk}))
        else:
            return render(request, 'registrar_recebedor.html', {'form' : form_recebedor})
    
class RegistrarEletricistaView(View):

    template_name = 'registrar_exemplo.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form_user = RegistrarEletricistaForm(request.POST, request.FILES)

        if form_user.is_valid():
            if request.FILES.get('foto'):
                foto = request.FILES.get('foto')
            else:
                foto = None
            dados_form = form_user.data
            

            if dados_form['tipo'] == 'Eletricista':
                usuario_eletri = User.objects.create_user(first_name=dados_form['nome'], email=dados_form['email'], password=dados_form['senha'], username=dados_form['nickname'])
                Coordenadas.objects.create(usuario=usuario_eletri, lat=-23.0, lng=-46.0)
                eletricista = Eletricista.objects.create(

                    usuario=usuario_eletri,
                    nascimento=dados_form['nascimento'],
                    telefone=dados_form['telefone'],
                    CEP=dados_form['CEP'],
                    CPF=dados_form['CPF'],
                    endereco=dados_form['endereco'],
                    genero=dados_form['genero'],
                    tipo=dados_form['tipo'],
                    foto=foto,
                    status='Inativo'
                )

                usuario = User.objects.get(username=dados_form['nickname'])
                usuario.is_active = False
                usuario.save()




                enviar_email('Sistema Eletricista24hrs', 
                 'Você, ' + dados_form['nome'] + ' foi registrado no nosso sistema, aguarde enquanto validamos seu cadastro',
                 settings.EMAIL_HOST_USER,
                 [usuario_eletri.email]
                )

                return HttpResponseRedirect(reverse('registrar_recebedor', kwargs={'user_pk': usuario_eletri.pk}))

            
            else:
                usuario_cliente = User.objects.create_user(username=dados_form['nickname'], email=dados_form['email'], password=dados_form['senha'], first_name=dados_form['nome'])
                Coordenadas.objects.create(usuario=usuario_cliente, lat=-23.0, lng=-46.0)
                cliente = Cliente.objects.create(
                    usuario=usuario_cliente,
                    nascimento=dados_form['nascimento'],
                    telefone=dados_form['telefone'],
                    CEP=dados_form['CEP'],
                    CPF=dados_form['CPF'],
                    endereco=dados_form['endereco'],
                    genero=dados_form['genero'],
                    tipo=dados_form['tipo'],
                    foto=foto
                )

                pagarme.authentication_key('ak_test_uSXZcO1zJua2nG3ZhjmiUwcwnxnCgM')

                customer_data = {
                  'external_id': dados_form['nickname'],
                  'name': dados_form['nome'],
                  'type': 'individual',
                  'country': 'br',
                  'email': dados_form['email'],
                  'documents': [
                    {
                      'type': 'cpf',
                      'number': dados_form['CPF'],
                    }
                  ],
                  'phone_numbers': [dados_form['telefone']],
                  'birthday': '1998-05-01',
                }
                try:
                    customer = pagarme.customer.create(customer_data)
                except:
                    print ('errrrrrrrrrou')
                    return HttpResponse('cpf inválido')

                cliente.pagarme_id = customer["id"]
                cliente.save()
                





                enviar_email('Sistema Eletricista24hrs', 
                 'Você, ' + dados_form['nome'] + ' foi cadastrado no Sistema Eletricista 24hrs. Estamos prontos para lhe ajudar :)',
                 settings.EMAIL_HOST_USER,
                 [usuario_cliente.email]
                )
            #return redirect('/user/registrar/cartao/' + dados_form['nickname'] + '/')
            return redirect('/user/index')
        else:
            return render(request, 'registrar_exemplo.html', {'form': form_user})

class QuestionarioView(View):

    template_name = 'questionario.html'
    def get(self, request, nome_eletricista):
        return render(request, self.template_name, {'nome_eletricista' : nome_eletricista})

    def post(self, request, nome_eletricista):

        form_questionario = QuestionarioForm(request.POST, request.FILES)
        if form_questionario.is_valid():
            if request.FILES.get('pdf'):
                pdf_curriculo = request.FILES.get('pdf')
            else:
                pdf_curriculo = None

            dados_questionario = form_questionario.data
            pontuacao = 0
            if dados_questionario['perguntaA'] == 'x':
                pontuacao = pontuacao + 1
            if dados_questionario['perguntaB'] == 'x':
                pontuacao = pontuacao + 1
            if dados_questionario['perguntaC'] == 'x':
                pontuacao = pontuacao + 1
            if dados_questionario['perguntaD'] == 'x':
                pontuacao = pontuacao + 1

            usuario_em_questao = User.objects.get(username=nome_eletricista)
            eletricista_avaliado = Eletricista.objects.get(usuario=usuario_em_questao)
            questionario = Questionario.objects.create(eletricista_avaliado=eletricista_avaliado, pontuacao=pontuacao, pdf=pdf_curriculo)
            
            return redirect('/user/registro_concluido')

        else:
            return render(request, 'questionario.html', {'form_questionario' : form_questionario, 'nome_eletricista' : nome_eletricista})

@login_required(login_url='/user/login/')
def adm(request):
    numero_eletricista = 0
    for eletricista in Eletricista.objects.all():
        if eletricista.status == 'Inativo':
            numero_eletricista = numero_eletricista + 1
    context = {
        'numero_notificacao_eletricista' : numero_eletricista
    }
    return render(request, 'dashboard_exemplo.html', context)   

@login_required(login_url='/user/login/')
def perfil_eletricista(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    eletricista_em_questao = Eletricista.objects.get(usuario=usuario_em_questao)
    questionario_em_questao = Questionario.objects.get(eletricista_avaliado=eletricista_em_questao)
    nome_curriculo = questionario_em_questao.pdf.name

    return render(request, 'perfil_eletricista.html', {'eletricista' : eletricista_em_questao, 'questionario': questionario_em_questao, 'curriculo' : nome_curriculo})

@login_required(login_url='/user/login/')
def perfil_cliente(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
    return render(request, 'perfil_cliente.html', {'cliente' : cliente_em_questao})

@login_required(login_url='/user/login/')
def questionarios_pendentes(request):
    context = {
        'questionario_list' : reversed(Questionario.objects.all())
    }
    return render(request, 'questionarios_pendentes.html', context)

@login_required(login_url='/user/login/')
def aceitar(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    usuario_em_questao.is_active = True
    usuario_em_questao.save()
    eletricista_aceito = Eletricista.objects.get(usuario=usuario_em_questao)
    eletricista_aceito.status = 'Ativo'
    eletricista_aceito.bloqueado = 'False'
    eletricista_aceito.save()
    enviar_email('Eletricista24hrs', 
                 'Você, ' + nickname + ' foi aceito no nosso sistema.',
                 settings.EMAIL_HOST_USER,
                 [usuario_em_questao.email]
                )

    return redirect('/user/adm/questionarios_pendentes')

@login_required(login_url='/user/login/')
def recusar(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    eletricista_recusado_model = Eletricista.objects.get(usuario=usuario_em_questao)
    eletricista_recusado_model.delete()
    eletricista_recusado_user = usuario_em_questao
    eletricista_recusado_user.delete()
    enviar_email('Sistema Eletricista24hrs', 
                 'Você, ' + nickname + ' foi recusado no nosso sistema',
                 settings.EMAIL_HOST_USER,
                 [usuario_em_questao.email] #aqui pode colocar o email da pessoa no caso, ou uma lista de varios emails
                )
    return redirect('/user/adm/questionarios_pendentes')

@login_required(login_url='/user/login/')
def eletricistas_registrados(request):
    eletricistas_registrados = Eletricista.objects.filter(status='Ativo')
    eletricistas_js = []
    for eletricista in eletricistas_registrados:
        eletricistas_js.append(eletricista.usuario.first_name)
    return render(request, 'eletricistas_registrados.html', {'eletricistas_registrados' : eletricistas_registrados, 'eletricistas_js' : eletricistas_js})

@login_required(login_url='/user/login/')
def bloquear_eletricista_registrado(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    eletricista_bloqueado = Eletricista.objects.get(usuario=usuario_em_questao)
    eletricista_bloqueado.bloqueado = 'True'
    eletricista_bloqueado.save()
    user_bloqueado = usuario_em_questao
    user_bloqueado.is_active = False
    user_bloqueado.save()
    enviar_email('Sistema Eletricista24hrs', 
                 'Você, ' + nickname + ' foi bloqueado do nosso sistema',
                 settings.EMAIL_HOST_USER,
                 [usuario_em_questao.email]
                )
    return redirect('/user/adm/eletricistas_registrados')

@login_required(login_url='/user/login/')
def desbloquear_eletricista_registrado(request, nickname):
    usuario_em_questao = User.objects.get(username=nickname)
    eletricista_desbloqueado = Eletricista.objects.get(usuario=usuario_em_questao)
    eletricista_desbloqueado.bloqueado = 'False'
    eletricista_desbloqueado.save()
    user_desbloqueado = usuario_em_questao
    user_desbloqueado.is_active = True
    user_desbloqueado.save()

    enviar_email('Sistema Eletricista24hrs', 
                 'Você, ' + nickname + ' foi desbloquado do nosso sistema',
                 settings.EMAIL_HOST_USER,
                 [usuario_em_questao.email]
                )
    return redirect('/user/adm/eletricistas_registrados')

class RegistrarAdministradorView(View):

    template_name = 'diegao.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form_user = RegistrarAdministradorForm(request.POST, request.FILES)
        if Admin.objects.filter(user=request.user).exists():

            if form_user.is_valid():
                dados_form = form_user.data

                usuario = User.objects.create_user(dados_form['nome'], dados_form['email'], dados_form['senha'])
                usuario.save()

                administrador = Admin.objects.create(
                    user = usuario,
                    nome = dados_form['nome'],
                    email=dados_form['email'],
                    senha=dados_form['senha'],
                    )
                administrador.save()

                return redirect('/user/adm/')
            else:
                return render(request, 'registrar_admin.html', {'form': form_user})
        else:
            return HttpResponse('voce nao é permitido a criar um administrador')

@login_required(login_url='/user/login/')
def clientes_registrados(request):
    clientes_registrados = Cliente.objects.all()
    clientes_js = []
    for cliente in clientes_registrados:
        clientes_js.append(cliente.usuario.first_name)
    return render(request, 'clientes_registrados.html', {'clientes_registrados' : clientes_registrados, 'clientes_js' : clientes_js})

#==============Recuperar Senha=============================================#

def password_reset(request, is_admin_site=False,
                   template_name='recuperar_senha.html',
                   email_template_name='email.html',
                   subject_template_name='assunto.html',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': 'Password reset',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def tela_inicial(request):
    return render(request, 'loginEletricista_exemplo.html')


def registro_concluido(request):
    return render(request, 'error-404.html')

def Base(request):
    return render(request, 'base_cliente.html')

@login_required(login_url='/user/login/')
def tela_cliente(request):
    return render(request, 'solicitar_servico.html', {"usuario" : request.user})

def tela_eletricista(request):
    return render(request, 'base_eletricista.html')

@login_required(login_url='/user/login/')
def ListarPedidos(request):
    
    pedidos = PedidoDeServico.objects.filter(cliente=request.user.username)
    #user o pedidos acima pra filtar apenas os servicos do cliente logado no momento
    context = {
     'pedidos' : pedidos
    }
    return render(request, 'listar_pedido_servico.html', context)

def dump(request):
    return render(request, 'dump.html')

@login_required(login_url='/user/login/')
def servico(request):
    servico_em_questao = PedidoDeServico.objects.get(id=len(PedidoDeServico.objects.all()))
    nickname_eletricista = servico_em_questao.eletricista
    user_eletricista = User.objects.get(username=nickname_eletricista)
    eletricista_avaliado = Eletricista.objects.get(usuario=user_eletricista)
    return render(request, 'servico2.html', {'eletricista' : eletricista_avaliado})

@login_required(login_url='/user/login/')
def servico_avaliar(request):
    
    servico_em_questao = PedidoDeServico.objects.get(id=len(PedidoDeServico.objects.all()))
    nickname_eletricista = servico_em_questao.eletricista
    user_eletricista = User.objects.get(username=nickname_eletricista)
    eletricista_avaliado = Eletricista.objects.get(usuario=user_eletricista)
    if request.method == 'POST':
        print (request.POST)
        nota = int(request.POST.get('nota'))
        #id_servico = int(request.POST.get('servico'))        
        if(eletricista_avaliado.nota == None):
            eletricista_avaliado.nota = nota
        else:
            eletricista_avaliado.nota = (eletricista_avaliado.nota + nota)/2
            print ('a nota ehhh', eletricista_avaliado.nota)
            eletricista_avaliado.save()

        return redirect('/user/index/')
    else:
        return render(request, 'avaliar2.html', {'eletricista' : eletricista_avaliado})

@login_required(login_url='/user/login/')
def avaliar(request):
    return render(request, 'servico_ws.html')

# def Perfil_do_cliente(request, nickname):
#   usuario_em_questao = User.objects.get(username=nickname)
#   cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
#   return render(request, 'Perfil_do_cliente.html', {'cliente' : cliente_em_questao})


class Perfil_do_cliente(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'Perfil_do_cliente.html'
    @method_decorator(login_required)
    def get(self, request, nickname):
        usuario_em_questao = User.objects.get(username=nickname)
        cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
        return render(request, 'Perfil_do_cliente.html', {'cliente' : cliente_em_questao})
    def post(self, request, nickname):

        if(request.POST.get("foto")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.foto = request.FILES.get("foto")
            cliente_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("nome")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            usuario_em_questao.first_name = request.POST.get("nome")
            usuario_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("CPF")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.CPF = request.POST.get("CPF")
            cliente_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("CEP")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.CEP = request.POST.get("CEP")
            cliente_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("endereco")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.endereco = request.POST.get("endereco")
            cliente_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("telefone")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.telefone = request.POST.get("telefone")
            cliente_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("email")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            usuario_em_questao.email = request.POST.get("email")
            usuario_em_questao.save()
            print(usuario_em_questao)
        if(request.POST.get("genero")):
            print(request.POST)
            usuario_em_questao = User.objects.get(username=nickname)
            cliente_em_questao = Cliente.objects.get(usuario=usuario_em_questao)
            cliente_em_questao.genero = request.POST.get("genero")
            cliente_em_questao.save()
            print(usuario_em_questao)
        return render(request, 'Perfil_do_cliente.html', {'cliente' : cliente_em_questao})  

















# http://localhost:8000/user/tela1/?id_servico=1&servico=1&preco_servico=123
class Tela1(View):
    def get(self, request, id_servico, valor_servico):

        servico_id = id_servico
        preco_servico = int(valor_servico)

        
        context = {
            "encryption_key": "ek_test_hlZxSmoUjPGs6sANAz6lCBoWT6FOWD",

            "id_servico": servico_id,
            "preco_servico": preco_servico,

        }

        #teste = Cliente.objects.get(usuario_id="1").nascimento
        #print(teste)

        return render(request, 'tela1.html', context)

    def post(self, request):
        pass



class Tela2(View):
    def get(self, request):
        data = json.loads(request.GET.get("data"))

        id_servico = request.GET.get("id_servico")
        servico = PedidoDeServico.objects.get(pk=id_servico)
        servico.status = 'Pago'
        servico.save()
        user_em_questao = User.objects.get(username=servico.eletricista)
        eletricista = Eletricista.objects.get(usuario=user_em_questao)
        #eletricista = Eletricista.objects.get(pk=servico.eletricista)
        preco_servico = request.GET.get("preco_servico")

        pagarme.authentication_key("ak_test_uSXZcO1zJua2nG3ZhjmiUwcwnxnCgM")



        # Billing Address obtain
        zip_code = request.GET.get("zip_code").replace("-", "")
        number = request.GET.get("number")
        state = request.GET.get("state")
        city = request.GET.get("city")
        neighbourhood = request.GET.get("neighbourhood")
        street = request.GET.get("street")


        cliente = Cliente.objects.get(usuario=request.user)
        year = str(cliente.nascimento.year)
        month = str(cliente.nascimento.month)
        if len(month) == 1:
            month = "0" + month
        day = str(cliente.nascimento.day)
        if len(day) == 1:
            day = "0" + day

        # Do transaction
        params = {
        
            "amount": data["amount"],
            "card_hash": data["card_hash"],
            "installments":data["installments"],
            "customer": {
                "external_id": str(cliente.pk),
                "name": cliente.usuario.first_name,
                "type": "individual",
                "country": "br",
                "email": cliente.usuario.email,
                "documents": [
                    {
                        "type": "cpf",
                        "number": cliente.CPF.replace(".", "").replace("-", "")
                    }
                ],
                "phone_numbers": ["+" + cliente.telefone.replace("(", "").replace(")", "").replace("-", "")],
                "birthday": year + "-" + month + "-" + day
            },
            "billing": {
                "name": "EXEMPLO",
                "address": {
                    "country": "br",
                    "state": state,
                    "city": city,
                    "neighborhood": neighbourhood,
                    "street": street,
                    "street_number": number,
                    "zipcode": zip_code
                }
            },
            "items": [
                {
                    "id": id_servico,
                    "title": "EXEMPLO",
                    "unit_price": data["amount"],
                    "quantity": "1",
                    "tangible": False
                }
            ],
            "split_rules": [
                {
                    "recipient_id": eletricista.pagarme_id,
                    "percentage": "100",
                    "liable": True,
                    "charge_processing_fee": True
                }
            ]
        }
        trx = pagarme.transaction.create(params)
        # ============================================
        # COLOCAR AQUI A ATUALIZACAO DE STATUS DO PEDIDO
        # ============================================
        return render(request, 'tela2.html')

    def post(self, request):
        pass

class Escolhe_Cadastro(View):
    def get(self, request):
        return render(request, 'escolhe_cadastro.html')
