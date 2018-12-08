from django.contrib import admin
from .eletricista.models import Eletricista
from .cliente.models import Cliente
from .models import Admin
from .models import ValorPorHora

# Register your models here.

admin.site.register(Admin)
admin.site.register(ValorPorHora)
