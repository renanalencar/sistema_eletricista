from django.db import models

# Create your models here.
class Cliente(models.Model):

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
	

	def __str__(self):
		return self.nome