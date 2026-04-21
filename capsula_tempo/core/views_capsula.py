from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.views import View

from .models import Capsula, ItemTexto
from .forms import CapsulaForm, CapsulaEdicaoForm
from .mixins import CapsulaEditMixin


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
                # Não criar objetos no GET. Se não existir ItemTexto, passar uma instância não persistida
                item = capsula.textos.first()
                if not item:
                    item = ItemTexto(capsula=capsula, texto='')
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
        raw_senha = form.cleaned_data.get('senha')
        texto = form.cleaned_data.get('texto')

        capsula = form.save(commit=False)
        if raw_senha:
            capsula.set_senha(raw_senha)
        capsula.save()

        if texto:
            ItemTexto.objects.create(capsula=capsula, texto=texto)

        self.object = capsula
        return redirect(self.get_success_url())


class DeletarCapsula(LoginRequiredMixin, DeleteView):
    model = Capsula
    success_url = reverse_lazy('lista')

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)

    def get(self, request, *args, **kwargs):
        return redirect(reverse('lista') + '?delete=' + str(kwargs['pk']))


class CapsulaDetail(LoginRequiredMixin, DetailView):
    model = Capsula
    template_name = 'capsula_detail.html'
    context_object_name = 'capsula'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)


class AutorizarEdicaoView(LoginRequiredMixin, CapsulaEditMixin, View):
    def post(self, request, pk):
        capsula = self.get_capsula(pk)

        if not capsula.pode_ser_editada():
            return redirect('lista')

        senha = request.POST.get('senha', '')

        if capsula.check_senha(senha):
            self.authorize_edit_session(capsula)
            return redirect(reverse('lista') + f'?edit_form={pk}')

        return redirect(reverse('lista') + f'?edit={pk}&wrong=1')


class EditarCapsulaView(LoginRequiredMixin, CapsulaEditMixin, View):
    def post(self, request, itemtexto_pk):
        item = ItemTexto.objects.filter(pk=itemtexto_pk, capsula__usuario=request.user).first()

        if item:
            capsula = item.capsula
        else:
            capsula = self.get_capsula(itemtexto_pk)
            item = capsula.textos.first()

        if not capsula.pode_ser_editada():
            return redirect('lista')

        if not self.is_edit_session_authorized(capsula):
            return redirect(reverse('lista') + f'?edit={capsula.pk}')

        form = CapsulaEdicaoForm(request.POST, instance=capsula)
        if not form.is_valid():
            return redirect(reverse('lista') + f'?edit_form={capsula.pk}&error=1')

        form.save(item=item)

        self.clear_edit_session(capsula)
        return redirect(reverse('lista'))
