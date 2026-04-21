from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views import View
from django.utils.dateparse import parse_date


from .models import Capsula, ItemTexto, Usuario
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

        edit_id = self.request.GET.get('edit')
        if edit_id:
            try:
                capsula = Capsula.objects.get(pk=edit_id, usuario=self.request.user)
                context['capsula_to_edit'] = capsula
                context['wrong_password'] = self.request.GET.get('wrong')
            except Capsula.DoesNotExist:
                pass

        edit_form_id = self.request.GET.get('edit_form')
        if edit_form_id:
            try:
                capsula = Capsula.objects.get(pk=edit_form_id, usuario=self.request.user)
                item = capsula.textos.first()
                if not item:
                    item = ItemTexto.objects.create(capsula=capsula, texto='')
                context['capsula_to_edit_form'] = capsula
                context['itemtexto_to_edit'] = item
                context['edit_error'] = self.request.GET.get('error')
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
        # set edit password (hashed) on creation
        raw_senha = form.cleaned_data.get('senha')
        response = super().form_valid(form)

        capsula = self.object
        if raw_senha:
            capsula.set_senha(raw_senha)
            capsula.save()

        if form.cleaned_data.get('texto'):
            ItemTexto.objects.create(capsula=capsula, texto=form.cleaned_data['texto'])

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

class AutorizarEdicaoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        capsula = get_object_or_404(Capsula, pk=pk, usuario=request.user)

        senha = request.POST.get('senha', '')

        if capsula.check_senha(senha):
            request.session[f'capsula_edit_{pk}'] = True
            request.session.modified = True
            return redirect(reverse('lista') + f'?edit_form={pk}')

        return redirect(reverse('lista') + f'?edit={pk}&wrong=1')

class EditarCapsulaView(LoginRequiredMixin, View):
    def post(self, request, itemtexto_pk):
        item = get_object_or_404(
            ItemTexto,
            pk=itemtexto_pk,
            capsula__usuario=request.user
        )

        capsula = item.capsula
        session_key = f'capsula_edit_{capsula.pk}'

        if not request.session.get(session_key):
            return redirect(reverse('lista') + f'?edit={capsula.pk}')

        texto = request.POST.get('texto', '').strip()
        titulo = request.POST.get('titulo', '').strip()
        data_abertura_str = request.POST.get('data_abertura', '').strip()

        if not texto or not titulo or not data_abertura_str:
            return redirect(reverse('lista') + f'?edit_form={capsula.pk}&error=1')

        data_abertura = parse_date(data_abertura_str)

        if not data_abertura:
            return redirect(reverse('lista') + f'?edit_form={capsula.pk}&error=1')

        item.texto = texto
        item.save()

        capsula.titulo = titulo
        capsula.data_abertura = data_abertura
        capsula.save()

        request.session.pop(session_key, None)

        return redirect(reverse('lista'))