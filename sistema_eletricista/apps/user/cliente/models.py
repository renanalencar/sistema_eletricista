from django.db import models

# Create your models here.
class ClienteManager(models.Manager):
	def BuscarCliente(self, query):
		return self.get_queryset().filter(models.Q(nome__icontains=query) | models.Q(nickname__icontains=query) | models.Q(email__icontains=query))
status = (('ativado', 'Ativado'), ('desativado','Desativado'))
class Cliente(models.Model):
	nome = models.CharField(max_length=50, null=False)
	nickname = models.CharField(max_length=50, null=False, default="w/e")
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)
	senha_novamente = models.CharField(max_length=30, null=False, default="w/e")
	telefone = models.IntegerField(null=False)
	CEP = models.IntegerField(null=False)
	CPF  = models.CharField(max_length=14, null=False)
	endereco = models.CharField(max_length=100, null=False)
	genero = models.CharField(max_length=255, null=False)
	tipo = models.CharField(max_length=12, null=False)
	foto = models.FileField(null=True, blank=True)
	status = models.CharField(max_length=10, null=False, default='ativado', choices = status)
	objects = ClienteManager()

	def __str__(self):
		return self.nome