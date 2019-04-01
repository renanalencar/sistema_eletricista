from django import forms
from django.contrib.auth.models import User
from .eletricista.models import *

class RegistrarEletricistaForm(forms.Form):

	nome = forms.CharField(required=True, max_length=50)
	nickname = forms.CharField(required=True, max_length=50)
	nascimento = forms.DateField(widget=forms.SelectDateWidget);
	email = forms.EmailField(required=True, max_length=50)
	senha = forms.CharField(required=True, max_length=30)
	senha_novamente = forms.CharField(required=True, max_length=30)
	telefone = forms.CharField(required=True)
	CEP = forms.CharField(required=True)
	CPF  = forms.CharField(required=True, max_length=14)
	endereco = forms.CharField(required=True, max_length=100)
	genero = forms.CharField(required=True)
	tipo = forms.CharField(required=True)
	foto = forms.FileField(required=False)



	def is_valid(self):
		valid = True
		if not super(RegistrarEletricistaForm, self).is_valid():
			self.adiciona_erro('Por favor verifique os dados informados')
			valid = False

		if self.data['senha_novamente'] != self.data['senha']:
			self.adiciona_erro('Senhas não iguais.')
			valid = False

		cpf_exists = Eletricista.objects.filter(CPF=self.data['CPF']).exists()
		if cpf_exists:
			self.adiciona_erro('CPF em uso, tente outro.')
			valid = False


		user_exists = User.objects.filter(username=self.data['nickname']).exists()
		if user_exists:
			self.adiciona_erro('Usuario ja existente.')
			valid = False
		return valid


	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)



class QuestionarioForm(forms.Form):
	perguntaA = forms.CharField(required=True, max_length=50)
	perguntaB = forms.CharField(required=True, max_length=50)
	perguntaC = forms.CharField(required=True, max_length=50)
	perguntaD = forms.CharField(required=True, max_length=50)
	perguntaE = forms.CharField(required=True, max_length=50)
	perguntaF = forms.CharField(required=True, max_length=50)
	pdf = forms.FileField(required=True)

	def is_valid(self):
		valid = True
		if not super(QuestionarioForm, self).is_valid():
			self.adiciona_erro('Por favor, preencha todo o questionário e envie seu currículo!')
			valid = False

		return valid

	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)


class RegistrarAdministradorForm(forms.Form):

	nome = forms.CharField(required=True, max_length=50)
	email = forms.EmailField(required=True, max_length=50)
	senha = forms.CharField(required=True, max_length=30)


	def is_valid(self):
		valid = True
		if not super(RegistrarAdministradorForm, self).is_valid():
			self.adiciona_erro('Por favor verifique os dados informados')
			valid = False

		user_exists = User.objects.filter(username=self.data['nome']).exists()

		if user_exists:
			self.adiciona_erro('Usuario ja existente')
			valid = False
		return valid

	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)

class RegistrarCartaoForm(forms.Form):

	card_number = forms.CharField(required=True)
	card_expiration_date = forms.CharField(required=True, max_length=10)
	card_cvv = forms.CharField(required=True)
	card_holder_name = forms.CharField(required=True, max_length=50)

	def is_valid(self):
		valid = True
		if not super(RegistrarCartaoForm, self).is_valid():
			self.adiciona_erro('Por favor verifique os dados informados')
			valid = False

		return valid

	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)

class RegistrarRecebedorForm(forms.Form):

	agencia = forms.IntegerField(required=True)
	# agencia_dv = forms.IntegerField(required=False)
	bank_code = forms.IntegerField(required=True)
	conta = forms.IntegerField(required=True)

	def is_valid(self):
		valid = True
		if not super(RegistrarRecebedorForm, self).is_valid():
			self.adiciona_erro('Por favor verifique os dados informados')
			valid = False

		return valid

	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)