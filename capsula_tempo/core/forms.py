from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Capsula, Usuario, ItemTexto, ItemImagem, ItemLink

class CapsulaForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea, required=False, label="Texto")
    imagem = forms.ImageField(required=False, label="Imagem")
    link = forms.URLField(required=False, label="Link")
    data_abertura = forms.DateTimeField(
        input_formats=[
            "%d/%m/%Y",
            "%d/%m/%y",
        ],
        label="Data de Abertura",
        error_messages={
            'invalid': 'Digite uma data válida (DD/MM/AAAA).',
            'required': 'Informe uma data.',
        }
    )

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

class UsuarioCriarForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']

class UsuarioAtualizarForm(UserChangeForm):
    password = None 

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']