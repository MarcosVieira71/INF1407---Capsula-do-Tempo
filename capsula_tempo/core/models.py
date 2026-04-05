from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    finalizada = models.BooleanField(default=False)
    
    def esta_aberta(self):
        return timezone.now() >= self.data_abertura

    def tem_conteudo(self):
        return (
            self.textos.exists() or
            self.imagens.exists() or
            self.links.exists()
        )
    
    def __str__(self):
        return self.titulo

    def clean(self):
        if self.data_abertura < timezone.now():
            raise ValidationError({
                'data_abertura': 'A data de abertura não pode estar no passado.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            original = Capsula.objects.filter(pk=self.pk).first()
            if original is not None:
                if (
                    original.titulo != self.titulo or
                    original.data_abertura != self.data_abertura or
                    original.usuario_id != self.usuario_id
                ):
                    raise ValueError('Cápsula não pode ser editada depois de criada.')
        super().save(*args, **kwargs)
    
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

