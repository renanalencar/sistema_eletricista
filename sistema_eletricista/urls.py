from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import sistema_eletricista.apps.user.urls
from sistema_eletricista import settings
from .apps.user import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	url('api/', include('sistema_eletricista.apps.api.urls')),
	url(r'^$', views.tela_inicial),
    url('user/', include('sistema_eletricista.apps.user.urls')),
    url('admin/', admin.site.urls),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += staticfiles_urlpatterns

