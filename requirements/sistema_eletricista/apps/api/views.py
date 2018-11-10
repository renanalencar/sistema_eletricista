from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import *
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

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



class EletricistaList(APIView):
	def get(self,request):
		eletricista=Eletricista.objects.all()
		serializer=EletricistaSerializer(eletricista ,many=True)
		print (serializer.data)
		return Response(serializer.data)
	def post(self,request):
		serializer = EletricistaSerializer(data=request.data)
		print('cheguei aqui primeiro')
		if serializer.is_valid():
			print('vim ate aqui')
			print (serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			print ('cheguei aqui')
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)