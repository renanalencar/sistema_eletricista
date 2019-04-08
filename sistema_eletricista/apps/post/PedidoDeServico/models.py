from django.db import models
from django.contrib.auth.models import User
from sistema_eletricista.apps.user.cliente.models import *
import datetime
from django.utils import timezone

class PedidoDeServico(models.Model):
	#data = models.DateTimeField('Data da solicitação', null=False, blank=False, default=datetime.datetime.now())
	data = timezone.now
	valor = models.FloatField('Valor', null=False, blank=False) #MEUDEUS chechar no futuro se precisa retirar
	endereco = models.CharField('Endereço', max_length=100, null=False)
	#cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
<<<<<<< HEAD
	cliente = models.CharField('Cliente', max_length=100, null=False)
	eletricista = models.CharField(max_length=100, null=False)
	status = models.CharField('Status', max_length=100, null=True, default="Nao pago (pendente)")
=======
	cliente = models.CharField('Cliente', max_length=100, null=False) #MEUDEUS verificar foreignkey
	eletricista = models.CharField(max_length=100, null=False) #MEUDEUS mudar para int verificar foreignkey
	status = models.CharField('Status', max_length=100, null=True, default="w/e")
>>>>>>> 63a71923f756ffc610d0aeb89cf481501b3f41d4
	

