from django.contrib import admin
from .models import Eletricista
from .models import Cliente

# Register your models here.

admin.site.register(Eletricista)
admin.site.register(Cliente)
