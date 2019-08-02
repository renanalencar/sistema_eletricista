from django.contrib import admin
from .eletricista.models import Eletricista
from .cliente.models import Cliente
from .models import Admin

# Register your models here.

admin.site.register(Admin)

