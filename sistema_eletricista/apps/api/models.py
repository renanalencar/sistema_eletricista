from django.db import models
from .serializers import *

# Create your models here.
def jwt_response_payload_handle(token, user=None, request=None):
	return {
		'token': token,
		'usuario': JwtUsuarioSerializer(user, context={'request':request}).data

	}