from django.contrib.auth.models import User
from rest_framework import serializers
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *

class EletricistaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Eletricista
		depth = 2
		fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cliente
		depth = 2
		fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class QuestionarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Questionario
		fields = '__all__'
		depth = 2