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
    template_name = 'login.html'


class UsuarioLogoutView(LogoutView):
    next_page = 'login'


class UsuarioCriaView(CreateView):
    model = Usuario
    form_class = UsuarioCriarForm
    template_name = 'registro.html'
    success_url = reverse_lazy('login')


class UsuarioAtualizaView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioAtualizarForm
    template_name = 'perfil.html'
    success_url = reverse_lazy('lista')

    def get_object(self):
        return self.request.user 


class HomeView(TemplateView):
    template_name = 'home.html'


class UsuarioPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class UsuarioPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class UsuarioPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UsuarioPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
