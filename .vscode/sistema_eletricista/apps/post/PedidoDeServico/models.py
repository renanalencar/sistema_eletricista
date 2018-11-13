from django.db import models
from django.contrib.auth.models import User
from sistema_eletricista.apps.user.cliente.models import *
import datetime

class PedidoDeServico(models.Model):
	data = models.DateTimeField('Data da solicitação', null=False, blank=False, default=datetime.datetime.now())
	valor = models.FloatField('Valor', null=False, blank=False)
	endereco = models.CharField('Endereço', max_length=100, null=False)
	#cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	cliente = models.CharField('Cliente', max_length=100, null=False)
	eletricista = models.CharField(max_length=100, null=False)
	

