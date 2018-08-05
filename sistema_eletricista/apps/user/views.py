from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrarEletricistaForm
from django.views.generic.base import View
from django.contrib.auth.models import User
from .eletricista.models import Eletricista
from .cliente.models import Cliente
from django.urls import reverse

# Create your views here.
@login_required
def get_usuario_logado(request):
	usuario = request.user
	eletricista_existe = Eletricista.objects.filter(nome=usuario).exists()
	if eletricista_existe:
		eletricista = Eletricista.objects.get(nome=usuario)
		return eletricista
	else:
		cliente = Cliente.objects.get(nome=usuario)
		return cliente

@login_required
def index(request):
	return render(request, 'logado_com_sucesso.html', {'usuario' : get_usuario_logado(request)})


class RegistrarEletricistaView(View):

	template_name = 'registrar_exemplo.html'
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		form_user = RegistrarEletricistaForm(request.POST, request.FILES)
		print (request.FILES)

		if form_user.is_valid():
			if request.FILES.get('foto'):
				foto = request.FILES.get('foto')
			else:
				foto = None
			dados_form = form_user.data

			usuario = User.objects.create_user(dados_form['nome'], dados_form['email'], dados_form['senha'])
			
			print (foto)

			if dados_form['tipo'] == 'Eletricista':
				eletricista = Eletricista.objects.create(
					nome=dados_form['nome'],
					email=dados_form['email'],
					senha=dados_form['senha'],
					telefone=dados_form['telefone'],
					CEP=dados_form['CEP'],
					CPF=dados_form['CPF'],
					endereco=dados_form['endereco'],
					genero=dados_form['genero'],
					tipo=dados_form['tipo'],
					foto=foto
				)
				print (eletricista.foto)
			else:
				cliente = Cliente.objects.create(
					nome=dados_form['nome'],
					email=dados_form['email'],
					senha=dados_form['senha'],
					telefone=dados_form['telefone'],
					CEP=dados_form['CEP'],
					CPF=dados_form['CPF'],
					endereco=dados_form['endereco'],
					genero=dados_form['genero'],
					tipo=dados_form['tipo'],
					foto=foto
				)
			return redirect('login')
		else:
			return render(request, 'registrar_exemplo.html', {'form': form_user})


			
		

