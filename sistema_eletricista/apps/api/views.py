from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import *
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response

class UsuarioViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UsuarioSerializer

class EletricistaViewSet(viewsets.ModelViewSet):
	queryset = Eletricista.objects.all()
	serializer_class = EletricistaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializer

	#@list_route(methods = ['get'])
	#def gatos(self, request):
	#	gatos = Perfil.objects.filter(tipo='Gato')
	#	gatos_json = RegistroSerializer(gatos, many=True)
	#	return Response(gatos_json.data)

	#@list_route(methods=['get'])
	#def caes(self, request):
	#	caes = Perfil.objects.filter(tipo='Cachorro')
	#	caes_json = RegistroSerializer(caes, many='True')
	#	return Response(gatos_json.data)
