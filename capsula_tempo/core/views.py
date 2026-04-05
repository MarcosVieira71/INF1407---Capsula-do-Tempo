from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from .models import Capsula

class ListaCapsulas(ListView):
    model = Capsula
    template_name = 'capsula_list.html'

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)
    
class CriarCapsula(LoginRequiredMixin, CreateView):
    model = Capsula
    fields = ['titulo', 'data_abertura']
    success_url = reverse_lazy('lista')
    template_name = 'capsula_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
class DeletarCapsula(DeleteView):
    model = Capsula
    success_url = reverse_lazy('lista')

    def get_queryset(self):
        return Capsula.objects.filter(usuario=self.request.user)