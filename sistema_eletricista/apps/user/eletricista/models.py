from django.db import models

# Create your models here.
class EletricistaManager(models.Manager):
	def BuscarEletricista(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(nickname__icontains=query) | models.Q(email__icontains=query))

class Eletricista(models.Model):

	nome = models.CharField(max_length=50, null=False)
	nickname = models.CharField(max_length=50, null=False, default='aleatorio')
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)
	senha_novamente = models.CharField(max_length=30, null=False, default='SOME STRING')
	telefone = models.IntegerField(null=False)
	CEP = models.IntegerField(null=False)
	CPF  = models.CharField(max_length=14, null=False)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	status = models.CharField(max_length=10, null=False, default='')
	bloqueado = models.CharField(max_length=10, null=False, default='False')
	objects = EletricistaManager()

	def __str__(self):
		return self.nome

class Questionario(models.Model):
	eletricista_avaliado = models.OneToOneField(Eletricista, on_delete=models.CASCADE, primary_key=True)
	pontuacao = models.IntegerField(null=False)
	pdf = models.FileField(null=True, blank=True)

