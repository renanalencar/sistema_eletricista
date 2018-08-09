from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#Create your models here.

class Admin(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	nome = models.CharField(max_length=50, null=False)
	email = models.EmailField(max_length=50, null=False)
	senha = models.CharField(max_length=30, null=False)


	def __str__(self):
		return self.nome



