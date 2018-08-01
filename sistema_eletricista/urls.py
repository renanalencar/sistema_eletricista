
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import sistema_eletricista.apps.user.urls
from sistema_eletricista import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url('user/', include('sistema_eletricista.apps.user.urls')),
    url('admin/', admin.site.urls),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns

