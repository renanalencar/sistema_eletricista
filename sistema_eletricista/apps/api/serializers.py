from django.contrib.auth.models import User
from rest_framework import serializers
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *

class EletricistaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Eletricista
		depth = 1
		fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cliente
		depth = 1
		fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'email', 'password', 'username', 'is_active')


class QuestionarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Questionario
		fields = '__all__'
		depth = 2