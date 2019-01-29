from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClienteManager(models.Manager):
	def BuscarCliente(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(nickname__icontains=query) | models.Q(email__icontains=query))

class Cliente(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	telefone = models.CharField(max_length=20, null=False)
	CEP = models.CharField(max_length=20, null=False)
	CPF  = models.CharField(max_length=14, null=False)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	nota = models.DecimalField(max_digits=5, decimal_places=3, null=True, default=None)
	objects = ClienteManager()
	pagarme_id = models.CharField(max_length=32, null=True, blank=True)
	
	def __str__(self):
		return self.usuario.first_name
