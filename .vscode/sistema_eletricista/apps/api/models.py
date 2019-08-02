from django.db import models
#from .serializers import EletricistaSerializer, ClienteSerializer
from sistema_eletricista.apps.api.serializers import *
from sistema_eletricista.apps.user.eletricista.models import *
from sistema_eletricista.apps.user.cliente.models import *
import json
from django.core import serializers
from django.contrib.auth.models import User
# Create your models here.

def jwt_response_payload_handle(token, user=None, request=None):

	if Eletricista.objects.filter(usuario=user).exists():
		return {
			'token': token,
			'eletricista': EletricistaSerializer(user.eletricista).data
		}
	else:
		return {
			'token': token,
			'cliente': ClienteSerializer(user.cliente).data
		}

