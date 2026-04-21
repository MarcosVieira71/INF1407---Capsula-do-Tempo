"""
Módulo de views para gestão de usuários e autenticação.

Este módulo centraliza as views de controle de acesso, incluindo login, logout,
registro de novos usuários, atualização de perfil e o fluxo completo de
recuperação de senha.
"""

from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Usuario
from .forms import UsuarioCriarForm, UsuarioAtualizarForm


class UsuarioLoginView(LoginView):
    """Exibe o formulário de login e autentica o usuário."""
    template_name = 'login.html'


class UsuarioLogoutView(LogoutView):
    """Encerra a sessão do usuário e redireciona para a página de login."""
    next_page = 'login'


class UsuarioCriaView(CreateView):
    """Gerencia a renderização do formulário e a persistência de novos usuários."""
    model = Usuario
    form_class = UsuarioCriarForm
    template_name = 'registro.html'
    success_url = reverse_lazy('login')


class UsuarioAtualizaView(LoginRequiredMixin, UpdateView):
    """
    Permite que o usuário autenticado atualize seus próprios dados de perfil.

    Utiliza o LoginRequiredMixin para garantir que apenas usuários logados
    acessem a view.
    """
    model = Usuario
    form_class = UsuarioAtualizarForm
    template_name = 'perfil.html'
    success_url = reverse_lazy('lista')

    def get_object(self):
        """Retorna o usuário logado atualmente para garantir que ele edite apenas o próprio perfil."""
        return self.request.user 


class HomeView(TemplateView):
    """Exibe a página inicial pública ou de boas-vindas do projeto."""
    template_name = 'home.html'


class UsuarioPasswordResetView(PasswordResetView):
    """Inicia o processo de recuperação de senha solicitando o e-mail do usuário."""
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class UsuarioPasswordResetDoneView(PasswordResetDoneView):
    """Exibe a confirmação de que o e-mail de recuperação foi enviado."""
    template_name = 'password_reset_done.html'


class UsuarioPasswordResetConfirmView(PasswordResetConfirmView):
    """Valida o token enviado por e-mail e permite a definição de uma nova senha."""
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UsuarioPasswordResetCompleteView(PasswordResetCompleteView):
    """Exibe a confirmação final de que a senha foi alterada com sucesso."""
    template_name = 'password_reset_complete.html'
