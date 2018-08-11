from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrarEletricistaForm
from .forms import QuestionarioForm
from django.views.generic.base import View
from django.contrib.auth.models import User
from .eletricista.models import Eletricista
from .cliente.models import Cliente
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Admin
from django.urls import reverse
from .eletricista.models import Eletricista, EletricistaManager
from .eletricista.models import Questionario
from .cliente.models import Cliente, ClienteManager
# Create your views here.


#Função de enviar emails
def enviar_email(subject, message, email_from, recipient_list):
	send_mail(subject, message, email_from, recipient_list)
	print ('enviei')
	return;


@login_required
def get_usuario_logado(request):
	usuario = request.user
	eletricista_existe = Eletricista.objects.filter(nickname=usuario).exists()
	if eletricista_existe:
		eletricista = Eletricista.objects.get(nickname=usuario)
		return eletricista
	else:
		cliente = Cliente.objects.get(nickname=usuario)
		return cliente


@login_required
def index(request):
	#subject = 'TESTE DO TESTE DO TESTE'
	#message = 'teste teste teste'
	#email_from = settings.EMAIL_HOST_USER
	#recipient_list = ['vinicius.roland@polijunior.com.br',]
	#enviar_email(subject, message, email_from, recipient_list)
	return render(request, 'logado_com_sucesso.html', {'usuario' : get_usuario_logado(request)})


def BuscaEletricista(request):
    q = request.GET.get('buscaEletricista')
    if q is not None:
        resultEletricista = Eletricista.objects.BuscarEletricista(q)
    return render(request, 'busca_eletricista.html', {'resultEletricista' : resultEletricista})



def BuscaCliente(request):
    q1 = request.GET.get('buscaCliente')
    if q1 is not None:
        resultCliente = Cliente.objects.BuscarCliente(q1)
    return render(request, 'busca_cliente.html', {'resultCliente': resultCliente})




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

				eletricista = Eletricista.objects.create(

					nome=dados_form['nome'],
					nickname=dados_form['nickname'],
					email=dados_form['email'],
					senha=dados_form['senha'],
					telefone=dados_form['telefone'],
					CEP=dados_form['CEP'],
					CPF=dados_form['CPF'],
					endereco=dados_form['endereco'],
					genero=dados_form['genero'],
					tipo=dados_form['tipo'],
					foto=foto,
					status='Inativo'
				)
				usuario = User.objects.create_user(dados_form['nickname'], dados_form['email'], dados_form['senha'])
				usuario.is_active = False
				usuario.save()
				enviar_email('Sistema Eletricista24hrs', 
				 'Você, ' + dados_form['nome'] + ' foi registrado no nosso sistema, aguarde enquanto validamos seu cadastro',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br']
				)
				
				return HttpResponseRedirect(reverse('questionario', kwargs={'nome_eletricista': dados_form['nickname']}))
			else:
				cliente = Cliente.objects.create(
					nome=dados_form['nome'],
					nickname=dados_form['nickname'],
					email=dados_form['email'],
					senha=dados_form['senha'],
					senha_novamente=dados_form['senha_novamente'],
					telefone=dados_form['telefone'],
					CEP=dados_form['CEP'],
					CPF=dados_form['CPF'],
					endereco=dados_form['endereco'],
					genero=dados_form['genero'],
					tipo=dados_form['tipo'],
					foto=foto
				)
				usuario = User.objects.create_user(dados_form['nickname'], dados_form['email'], dados_form['senha'])
				enviar_email('Sistema Eletricista24hrs', 
				 'Você, ' + dados_form['nome'] + ' foi cadastrado no Sistema Eletricista 24hrs. Estamos prontos para lhe ajudar :)',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br']
				)
			return redirect('login')
		else:
			return render(request, 'registrar_exemplo.html', {'form': form_user})



class QuestionarioView(View):

	template_name = 'questionario.html'
	def get(self, request, nome_eletricista):
		return render(request, self.template_name, {'nome_eletricista' : nome_eletricista})

	def post(self, request, nome_eletricista):

		form_questionario = QuestionarioForm(request.POST, request.FILES)

		if request.FILES.get('pdf'):
			pdf_curriculo = request.FILES.get('pdf')
		else:
			pdf_curriculo = None

		dados_questionario = form_questionario.data
		pontuacao = 0
		if dados_questionario['perguntaA'] == 'Correta':
			pontuacao = pontuacao + 1
		if dados_questionario['perguntaB'] == 'Correta':
			pontuacao = pontuacao + 1
		if dados_questionario['perguntaC'] == 'Correta':
			pontuacao = pontuacao + 1
		if dados_questionario['perguntaD'] == 'Correta':
			pontuacao = pontuacao + 1
		
		eletricista_avaliado = Eletricista.objects.get(nickname=nome_eletricista)
		questionario = Questionario.objects.create(eletricista_avaliado=eletricista_avaliado, pontuacao=pontuacao, pdf=pdf_curriculo)

		return HttpResponse('Obrigado por completar o cadastro, aguarde nossa revisão.')


def adm(request):
	numero_eletricista = 0
	for eletricista in Eletricista.objects.all():
		if eletricista.status == 'Inativo':
			numero_eletricista = numero_eletricista + 1
	context = {
		'numero_notificacao_eletricista' : numero_eletricista
	}
	return render(request, 'dashboard_exemplo.html', context)	
	
def perfil_eletricista(request, nickname):
	eletricista_em_questao = Eletricista.objects.get(nickname=nickname)
	questionario_em_questao = Questionario.objects.get(eletricista_avaliado=eletricista_em_questao)
	nome_curriculo = questionario_em_questao.pdf.name

	return render(request, 'perfil_eletricista.html', {'eletricista' : eletricista_em_questao, 'questionario': questionario_em_questao, 'curriculo' : nome_curriculo})

def perfil_cliente(request, nickname):
	cliente_em_questao = Cliente.objects.get(nickname=nickname)
	return render(request, 'perfil_cliente.html', {'cliente' : cliente_em_questao})

def questionarios_pendentes(request):
	context = {
		'questionario_list' : reversed(Questionario.objects.all())
	}
	return render(request, 'questionarios_pendentes.html', context)

def aceitar(request, nickname):
	usuario_aceito = User.objects.get(username=nickname)
	usuario_aceito.is_active = True
	usuario_aceito.save()
	eletricista_aceito = Eletricista.objects.get(nickname=nickname)
	eletricista_aceito.status = 'Ativo'
	eletricista_aceito.bloqueado = 'False'
	eletricista_aceito.save()
	enviar_email('Eletricista24hrs', 
				 'Você, ' + nickname + ' foi aceito no nosso sistema.',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br']
				)

	return redirect('/user/adm/questionarios_pendentes')
	
def recusar(request, nickname):
	eletricista_recusado_model = Eletricista.objects.get(nickname=nickname)
	eletricista_recusado_model.delete()
	eletricista_recusado_user = User.objects.get(username=nickname)
	eletricista_recusado_user.delete()
	enviar_email('Sistema Eletricista24hrs', 
				 'Você, ' + nickname + ' foi recusado no nosso sistema',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br'] #aqui pode colocar o email da pessoa no caso, ou uma lista de varios emails
				)
	return redirect('/user/adm/questionarios_pendentes')

def eletricistas_registrados(request):
	eletricistas_registrados = Eletricista.objects.filter(status='Ativo')
	return render(request, 'eletricistas_registrados.html', {'eletricistas_registrados' : eletricistas_registrados})

def bloquear_eletricista_registrado(request, nickname):
	eletricista_bloqueado = Eletricista.objects.get(nickname=nickname)
	eletricista_bloqueado.bloqueado = 'True'
	eletricista_bloqueado.save()
	print (eletricista_bloqueado.bloqueado)
	enviar_email('Sistema Eletricista24hrs', 
				 'Você, ' + nickname + ' foi bloqueado do nosso sistema',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br']
				)
	return redirect('/user/adm/eletricistas_registrados')


def desbloquear_eletricista_registrado(request, nickname):
	eletricista_desbloqueado = Eletricista.objects.get(nickname=nickname)
	eletricista_desbloqueado.bloqueado = 'False'
	eletricista_desbloqueado.save()
	print (eletricista_desbloqueado.bloqueado)
	enviar_email('Sistema Eletricista24hrs', 
				 'Você, ' + nickname + ' foi desbloquado do nosso sistema',
				 settings.EMAIL_HOST_USER,
				 ['pedro.medeiros@polijunior.com.br']
				)
	return redirect('/user/adm/eletricistas_registrados')


class RegistrarAdministradorView(View):

	template_name = 'registrar_exemplo.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated() & Admin.objects.filter(user=user).exists():
			form_user = RegistrarAdministradorForm(request.POST, request.FILES)
			print (request.FILES)

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

			return redirect('/login')
		else:
			return render(request, 'registrar_admin.html', {'form': form_user})

def clientes_registrados(request):
	clientes_registrados = Cliente.objects.all()
	return render(request, 'clientes_registrados.html', {'clientes_registrados' : clientes_registrados})

