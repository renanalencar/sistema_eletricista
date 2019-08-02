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
from django.http import HttpResponse, request, HttpResponseRedirect

class CoordenadasViewSet(viewsets.ModelViewSet):
	queryset = Coordenadas.objects.all()
	serializer_class = CoordenadasSerializer

class CoordsViewSet(APIView):
	def get(self, request, nickname):
		user_ = User.objects.get(username=nickname)
		coords = Coordenadas.objects.get(usuario=user_)
		serializer = CoordenadasSerializer(coords)
		return Response(serializer.data)
	def patch(self, request, nickname):
		user_ = User.objects.get(username=nickname)
		coords = Coordenadas.objects.get(usuario=user_)
		print (request.data)
		serializer = CoordenadasSerializer(coords, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		print (serializer.errors)
		return HttpResponse('errrou')

	
	
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



