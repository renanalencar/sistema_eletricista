
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import sistema_eletricista.apps.user.urls

urlpatterns = [
    #url('user/', include(sistema_eletricista.apps.user.urls)),
    url('admin/', admin.site.urls),
]

