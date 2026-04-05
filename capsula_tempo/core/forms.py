from django import forms
from .models import Capsula, ItemTexto, ItemImagem, ItemLink

class CapsulaForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea, required=False, label="Texto")
    imagem = forms.ImageField(required=False, label="Imagem")
    link = forms.URLField(required=False, label="Link")

    class Meta:
        model = Capsula
        fields = ['titulo', 'data_abertura']

    def clean(self):
        cleaned_data = super().clean()
        texto = cleaned_data.get('texto')
        imagem = cleaned_data.get('imagem')
        link = cleaned_data.get('link')

        if not texto and not imagem and not link:
            raise forms.ValidationError("Você deve adicionar pelo menos um conteúdo (texto, imagem ou link) à cápsula.")

        return cleaned_data