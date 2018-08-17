from django.conf.urls import url, include
from rest_framework import routers
from .views import EletricistaViewSet, ClienteViewSet, UsuarioViewSet
from .serializers import *

router = routers.DefaultRouter()
router.register(r'eletricistas', EletricistaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = router.urls
