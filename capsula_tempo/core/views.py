from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .models import Capsula, ItemTexto, ItemImagem, ItemLink, Usuario
from .forms import CapsulaForm, UsuarioCriarForm, UsuarioAtualizarForm

class ListaCapsulas(LoginRequiredMixin, ListView):
    model = Capsula
    template_name = 'capsula_list.html'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_id = self.request.GET.get('delete')
        if delete_id:
            try:
                capsula = Capsula.objects.get(pk=delete_id, usuario=self.request.user)
                context['capsula_to_delete'] = capsula
            except Capsula.DoesNotExist:
                pass
        return context
    
class CriarCapsula(LoginRequiredMixin, CreateView):
    model = Capsula
    form_class = CapsulaForm
    success_url = reverse_lazy('lista')
    template_name = 'capsula_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.finalizada = True
        response = super().form_valid(form)
        
        capsula = self.object
        if form.cleaned_data.get('texto'):
            ItemTexto.objects.create(capsula=capsula, texto=form.cleaned_data['texto'])
        if form.cleaned_data.get('imagem'):
            ItemImagem.objects.create(capsula=capsula, imagem=form.cleaned_data['imagem'])
        if form.cleaned_data.get('link'):
            ItemLink.objects.create(capsula=capsula, link=form.cleaned_data['link'])
        
        return response
    
class DeletarCapsula(LoginRequiredMixin, DeleteView):
    model = Capsula
    success_url = reverse_lazy('lista')

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)

    def get(self, request, *args, **kwargs):
        # Redirect GET requests to the list page with delete parameter
        return redirect(reverse('lista') + '?delete=' + str(kwargs['pk']))

class CapsulaDetail(LoginRequiredMixin, DetailView):
    model = Capsula
    template_name = 'capsula_detail.html'
    context_object_name = 'capsula'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)

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

