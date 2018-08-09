from django.contrib import admin
from .models import Eletricista
from .models import Cliente
from .models import Admin

# Register your models here.

admin.site.register(Eletricista)
admin.site.register(Cliente)
admin.site.register(Admin)