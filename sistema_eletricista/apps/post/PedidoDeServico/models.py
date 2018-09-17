from django.db import models
from django.contrib.auth.models import User
from sistema_eletricista.apps.user.cliente.models import *
import datetime

class PedidoDeServico(models.Model):
	data = models.DateTimeField('Data da solicitação', null=False, blank=False,default=datetime.datetime.now)
	aceito = models.BooleanField('Pedido aceito', default=False)
	valor = models.FloatField('Valor', null=False, blank=False)
	endereco = models.CharField('Endereço', max_length=100, null=False)
	CEP = models.CharField('CEP', max_length=20, null=False)
	visitado = models.BooleanField('Visitado', default=False)
	descricao = models.TextField('Descrição',null=True, default=None)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

