from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from .serializers import *
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token, obtain_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'eletricistas', EletricistaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'questionarios', QuestionarioViewSet)
router.register(r'coordenadas', CoordenadasViewSet)
urlpatterns = [
	url(r'^login/$', obtain_jwt_token),
	url(r'^token-verify/$', obtain_jwt_token),
	url(r'^token-refresh/$', obtain_jwt_token),
	url(r'^coords/(?P<nickname>\w+)/$', CoordsViewSet.as_view()),
        url(r'^editar_eletricista/(?P<nickname>\w+)/$', EditarElecViewSet.as_view())
]

urlpatterns += router.urls
#urlpatterns = format_suffix_patterns(urlpatterns)
