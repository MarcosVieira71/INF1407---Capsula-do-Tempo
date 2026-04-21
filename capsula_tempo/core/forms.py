"""
Definição dos formulários do sistema.

Este módulo contém os formulários para criação e edição de cápsulas, 
além da gestão de usuários, incluindo validações customizadas de dados 
e manipulação de instâncias relacionadas.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Capsula, Usuario, ItemTexto

class CapsulaForm(forms.ModelForm):
    """Formulário para a criação de novas instâncias de Capsula."""
    texto = forms.CharField(widget=forms.Textarea, required=True, label="Texto")
    senha = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha de edição")
    data_abertura = forms.DateField(
        input_formats=[
            "%Y-%m-%d",
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
        """Valida se o conteúdo textual da cápsula foi fornecido, além dos campos do modelo."""
        cleaned_data = super().clean()
        texto = cleaned_data.get('texto')

        if not texto:
            raise forms.ValidationError("Você deve adicionar um texto à cápsula.")

        return cleaned_data

class UsuarioCriarForm(UserCreationForm):
    """Formulário personalizado para o registro de novos usuários no sistema."""
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
    """Formulário para edição dos dados básicos do perfil do usuário."""
    password = None 

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']


class CapsulaEdicaoForm(forms.ModelForm):
    """Formulário especializado para a modificação de cápsulas existentes."""
    texto = forms.CharField(widget=forms.Textarea, required=True, label="Texto")
    data_abertura = forms.DateField(
        input_formats=[
            "%Y-%m-%d",
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
        """Garante que a cápsula não fique sem conteúdo textual durante a edição."""
        cleaned_data = super().clean()
        texto = cleaned_data.get('texto')

        if not texto:
            raise forms.ValidationError("Você deve adicionar um texto à cápsula.")

        return cleaned_data

    def save(self, commit=True, item=None):
        """
        Salva as alterações da cápsula e atualiza ou cria o ItemTexto associado.

        Args:
            commit (bool): Se verdadeiro, salva a instância no banco de dados.
            item (ItemTexto, optional): A instância de texto existente a ser editada.

        Returns:
            Capsula: A instância da cápsula atualizada.
        """
        capsula = super().save(commit=False)

        if commit:
            capsula.save()

        texto = self.cleaned_data.get('texto')

        if item and getattr(item, 'pk', None):
            item.texto = texto
            item.save()
        else:
            ItemTexto.objects.create(capsula=capsula, texto=texto)

        return capsula