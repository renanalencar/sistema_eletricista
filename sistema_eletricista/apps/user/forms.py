from django import forms
from django.contrib.auth.models import User

class RegistrarEletricistaForm(forms.Form):

	nome = forms.CharField(required=True, max_length=50)
	nickname = forms.CharField(required=True, max_length=50)
	email = forms.EmailField(required=True, max_length=50)
	senha = forms.CharField(required=True, max_length=30)
	senha_novamente = forms.CharField(required=True, max_length=30)
	telefone = forms.IntegerField(required=True)
	CEP = forms.IntegerField(required=True)
	CPF  = forms.CharField(required=True, max_length=14)
	endereco = forms.CharField(required=True, max_length=100)
	#genero = forms.MultipleChoiceField(choices=('Masculino', 'Feminino'), required=True)
	genero = forms.CharField(required=True)
	#tipo = forms.MultipleChoiceField(choices=('Eletricista', 'Cliente'), required=True)
	tipo = forms.CharField(required=True)
	foto = forms.FileField(required=False)



	def is_valid(self):
		valid = True
		if not super(RegistrarEletricistaForm, self).is_valid():
			self.adiciona_erro('Por favor verifique os dados informados')
			valid = False

		if self.data['senha_novamente'] != self.data['senha']:
			self.adiciona_erro('Senhas não iguais')
			valid = False

		user_exists = User.objects.filter(username=self.data['nickname']).exists()
		if user_exists:
			self.adiciona_erro('Usuario ja existente')
			valid = False
		return valid


	def adiciona_erro(self, message):
		erros = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		erros.append(message)


class QuestionarioForm(forms.Form):
	pontuacao = forms.CharField(required=True, max_length=50)