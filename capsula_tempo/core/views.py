from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from .models import Capsula, ItemTexto, ItemImagem, ItemLink
from .forms import CapsulaForm

class ListaCapsulas(LoginRequiredMixin, ListView):
    model = Capsula
    template_name = 'capsula_list.html'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)
    
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
    template_name = 'capsula_confirm_delete.html'
    success_url = reverse_lazy('lista')

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)

class CapsulaDetail(LoginRequiredMixin, DetailView):
    model = Capsula
    template_name = 'capsula_detail.html'
    context_object_name = 'capsula'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)
