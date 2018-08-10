from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#Create your models here.

class Admin(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	nome = models.CharField(max_length=50, null=False)
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)


	def __str__(self):
		return self.nome

class EletricistaManager(models.Manager):
	def BuscarEletricista(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(user__username__icontains=query) | models.Q(email__icontains=query))


class Eletricista(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	nome = models.CharField(max_length=50, null=False)
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)
	telefone = models.IntegerField(null=False)
	CEP = models.IntegerField(null=False)
	CPF  = models.CharField(max_length=14, null=False)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	objects = EletricistaManager()
	

	def __str__(self):
		return self.nome


class ClienteManager(models.Manager):
	def BuscarCliente(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(user__username__icontains=query) | models.Q(email__icontains=query))

class Cliente(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	nome = models.CharField(max_length=50, null=False)
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)
	telefone = models.IntegerField(null=False)
	CEP = models.IntegerField(null=False)
	CPF  = models.CharField(max_length=14, null=False)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	objects = ClienteManager()
	

	def __str__(self):
		return self.nome
