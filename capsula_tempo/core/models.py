from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Capsula(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capsulas')
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    data_abertura = models.DateTimeField()

    imagem = models.ImageField(upload_to='capsulas/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

