from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
from sistema_eletricista.apps.post.PedidoDeServico.models import *
from sistema_eletricista.apps.user.models import Coordenadas

class PedidoDeServicoSerializer(serializers.ModelSerializer):
	class Meta:
		model = PedidoDeServico
		fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'email', 'password', 'username', 'is_active')
		extra_kwargs = {
				'username': {
					'validators': [UnicodeUsernameValidator()],
					}
                }

class EletricistaSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(required=False)
	class Meta:
		model = Eletricista
		depth = 2
		fields = ('telefone', 'CEP', 'CPF', 'endereco', 'genero', 'tipo', 'status', 'bloqueado', 'foto', 'usuario', 'nota')

	def create(self, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		eletricista = Eletricista.objects.create(**validated_data)  
 
		return eletricista

	def update(self, instance, validated_data):

		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None


		instance.telefone = validated_data.get('telefone', instance.telefone)
		instance.CEP = validated_data.get('CEP', instance.CEP)
		instance.CPF = validated_data.get('CPF', instance.CPF)
		instance.endereco = validated_data.get('endereco', instance.endereco)
		instance.genero = validated_data.get('genero', instance.genero)
		instance.tipo = validated_data.get('tipo', instance.tipo)
		instance.status = validated_data.get('status', instance.status)
		instance.bloqueado = validated_data.get('bloqueado', instance.bloqueado)
                #instance.nota = validated_gata.get('nota', instance.nota)
		if(usuario != None):
			instance.usuario = validated_data.get('usuario')
		instance.save()
		return instance

class ClienteSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(required=True)
	class Meta:
		model = Cliente
		depth = 2
		fields = ('telefone', 'CEP', 'CPF', 'endereco', 'genero', 'tipo', 'foto', 'usuario', 'nota')

	def create(self, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		cliente = Cliente.objects.create(**validated_data)  
 
		return cliente
	def update(self, instance, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		instance.telefone = validated_data.get('telefone', instance.telefone)
		instance.CEP = validated_data.get('CEP', instance.CEP)
		instance.CPF = validated_data.get('CPF', instance.CPF)
		instance.endereco = validated_data.get('endereco', instance.endereco)
		instance.genero = validated_data.get('genero', instance.genero)
		instance.tipo = validated_data.get('tipo', instance.tipo)
		#instance.status = validated_data.get('status', instance.status)
        #instance.bloqueado = validated_data.get('bloqueado', instance.bloqueado)
		instance.nota = validated_data.get('nota', instance.nota)
		if(usuario != None):
			instance.usuario = validated_data.get('usuario')

		instance.save()
		return instance



class QuestionarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Questionario
		fields = '__all__'
		depth = 2

class CoordenadasSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(required=False)
	class Meta:
		model = Coordenadas
		fields = ('usuario', 'lat', 'lng')
	def create(self, validated_data):
		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None

		coordenadas = Coordenadas.objects.create(**validated_data)  
 
		return coordenadas

	def update(self, instance, validated_data):

		if(validated_data.get('usuario')):
			usuario_data = validated_data.pop('usuario')
			usuario = User.objects.create(**usuario_data)
			validated_data['usuario'] = usuario
		else:
			usuario = None
		if(usuario != None):
			instance.usuario = validated_data.get('usuario')
		instance.lat = validated_data.get('lat', instance.lat)
		instance.lng = validated_data.get('lng', instance.lng)
		instance.save()
		return instance



