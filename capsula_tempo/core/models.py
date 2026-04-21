from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Capsula(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capsulas')
    titulo = models.CharField(max_length=100)
    data_abertura = models.DateField()
    criada_em = models.DateField(auto_now_add=True)
    senha = models.CharField(max_length=128, null=True, blank=True)
    
    def esta_aberta(self):
        return timezone.localdate() >= self.data_abertura

    def tem_conteudo(self):
        return self.textos.exists()
    
    def pode_ser_editada(self):
        return not self.esta_aberta()
    
    def __str__(self):
        return self.titulo

    def clean(self):
        if not self.data_abertura:
            return 
            
        if self.data_abertura < timezone.localdate():
            raise ValidationError({
                'data_abertura': 'A data de abertura não pode estar no passado.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            original = Capsula.objects.filter(pk=self.pk).first()

            if original is not None:
                if original.usuario_id != self.usuario_id:
                    raise ValueError('Usuário da cápsula não pode ser alterado.')

                if original.senha and self.senha != original.senha:
                    self.senha = original.senha

        super().save(*args, **kwargs)

    def set_senha(self, raw_password):
        if raw_password:
            self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        if not self.senha:
            return False
        return check_password(raw_password, self.senha)
    
class ItemTexto(models.Model):
    capsula = models.ForeignKey(Capsula, on_delete=models.CASCADE, related_name='textos')
    criado_em = models.DateField(auto_now_add=True)
    texto = models.TextField()
