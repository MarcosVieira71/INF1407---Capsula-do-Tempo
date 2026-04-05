from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Capsula(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capsulas')
    titulo = models.CharField(max_length=100)
    data_abertura = models.DateTimeField()
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class ItemTexto(models.Model):
    capsula = models.ForeignKey(Capsula, on_delete=models.CASCADE, related_name='textos')
    criado_em = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()

class ItemImagem(models.Model):
    capsula = models.ForeignKey(Capsula, on_delete=models.CASCADE, related_name='imagens')
    criado_em = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='capsulas/')

class ItemLink(models.Model):
    capsula = models.ForeignKey(Capsula, on_delete=models.CASCADE, related_name='links')
    criado_em = models.DateTimeField(auto_now_add=True)
    link = models.URLField()

