from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EletricistaManager(models.Manager):
	def BuscarEletricista(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(nickname__icontains=query) | models.Q(email__icontains=query))

class Eletricista(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	nascimento = models.DateField(null=True, blank=False)
	telefone = models.CharField(max_length=20, null=False)
	CEP = models.CharField(max_length=20, null=False)
	CPF  = models.CharField(max_length=14, null=True)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	status = models.CharField(max_length=10, null=False, default='')
	bloqueado = models.CharField(max_length=10, null=False, default='False')
	nota = models.DecimalField(max_digits=5, decimal_places=3, null=True, default=None)
	objects = EletricistaManager()
	pagarme_id = models.CharField(max_length=32, null=True, blank=True)

	def __str__(self):
		return self.usuario.first_name

class Questionario(models.Model):
	eletricista_avaliado = models.OneToOneField(Eletricista, on_delete=models.CASCADE, default=None)
	pontuacao = models.IntegerField(null=False, default=None)
	pdf = models.FileField(null=True, blank=True)

