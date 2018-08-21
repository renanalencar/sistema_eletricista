from django.conf.urls import url, include
from rest_framework import routers
from .views import EletricistaViewSet, ClienteViewSet, UsuarioViewSet
from .serializers import *
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token, obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'eletricistas', EletricistaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
urlpatterns = [
	url(r'^login/$', obtain_jwt_token),
	url(r'^token-verify/$', obtain_jwt_token),
	url(r'^token-refresh/$', obtain_jwt_token)
]

urlpatterns += router.urls
