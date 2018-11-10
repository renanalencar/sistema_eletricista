from django.contrib.auth.models import User
from rest_framework import serializers
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'email', 'password', 'username', 'is_active')

class EletricistaSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(required=False)
	class Meta:
		model = Eletricista
		depth = 2
		fields = ('telefone', 'CEP', 'CPF', 'endereco', 'genero', 'tipo', 'status', 'bloqueado', 'usuario')

	def create(self, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		eletricista = Eletricista.objects.create(**validated_data)  
 
		return eletricista

class ClienteSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(required=True)
	class Meta:
		model = Cliente
		depth = 2
		fields = ('telefone', 'CEP', 'CPF', 'endereco', 'genero', 'tipo', 'usuario')

	def create(self, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		cliente = Cliente.objects.create(**validated_data)  
 
		return cliente


class QuestionarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Questionario
		fields = '__all__'
		depth = 2

