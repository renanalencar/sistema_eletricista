from django.contrib import admin
from .eletricista.models import Eletricista
from .cliente.models import Cliente

# Register your models here.

admin.site.register(Eletricista)
admin.site.register(Cliente)
