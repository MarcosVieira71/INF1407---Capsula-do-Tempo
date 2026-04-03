from django.db import models

class Capsula(models.Model):
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    data_abertura = models.DateTimeField()

    imagem = models.ImageField(upload_to='capsulas/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo