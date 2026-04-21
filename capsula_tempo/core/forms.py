from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Capsula, Usuario, ItemTexto

class CapsulaForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea, required=True, label="Texto")
    senha = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha de edição")
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

        if not texto:
            raise forms.ValidationError("Você deve adicionar um texto à cápsula.")

        return cleaned_data

class UsuarioCriarForm(UserCreationForm):
    username = forms.CharField(
        help_text = ''
    )

    password1 = forms.CharField(
    label = "Senha",
    widget = forms.PasswordInput,
    help_text = ''
    )

    password2 = forms.CharField(
        label ="Confirme a senha",
        widget =forms.PasswordInput,
        help_text=''
    )

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']

class UsuarioAtualizarForm(UserChangeForm):
    password = None 

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']