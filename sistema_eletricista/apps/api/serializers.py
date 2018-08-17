from django.contrib.auth.models import User
from rest_framework import serializers
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *

class EletricistaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Eletricista
		fields = '__all__'
		depth = 2

class ClienteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cliente
		fields = '__all__'
		depth = 2

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

