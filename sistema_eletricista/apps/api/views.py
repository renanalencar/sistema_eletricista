from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import *
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
from sistema_eletricista.apps.user.models import *
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

class CoordenadasViewSet(viewsets.ModelViewSet):
	queryset = Coordenadas.objects.all()
	serializer_class = CoordenadasSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UsuarioSerializer

class EletricistaViewSet(viewsets.ModelViewSet):
	queryset = Eletricista.objects.all()
	serializer_class = EletricistaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializer

class QuestionarioViewSet(viewsets.ModelViewSet):
	queryset = Questionario.objects.all()
	serializer_class = QuestionarioSerializer



