"""
Módulo de views para o gerenciamento do ciclo de vida das Cápsulas.

Este módulo lida com a listagem dinâmica, criação com hash de senha,
exclusão protegida e o fluxo de edição que exige validação de credenciais
temporárias em sessão.
"""

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.views import View

from .models import Capsula, ItemTexto
from .forms import CapsulaForm, CapsulaEdicaoForm
from .mixins import CapsulaEditMixin


class ListaCapsulas(LoginRequiredMixin, ListView):
    """Exibe todas as cápsulas pertencentes ao usuário logado e gerencia estados de modais via parâmetros GET."""
    model = Capsula
    template_name = 'capsula_list.html'

    def get_queryset(self):
        """Retorna apenas as cápsulas de propriedade do usuário atual."""
        return Capsula.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        """Injeta no template objetos para modais de exclusão, autenticação de edição e formulários de alteração baseados na URL."""
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
    """View para criação de novas cápsulas, tratando a persistência do autor e do conteúdo textual inicial."""
    model = Capsula
    form_class = CapsulaForm
    success_url = reverse_lazy('lista')
    template_name = 'capsula_form.html'

    def form_valid(self, form):
        """Associa o usuário logado à cápsula, processa o hash da senha e cria o ItemTexto inicial."""
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
    """Remove uma cápsula do banco de dados."""
    model = Capsula
    success_url = reverse_lazy('lista')

    def get_queryset(self):
        """Garante que o usuário só possa deletar suas próprias cápsulas."""
        return Capsula.objects.filter(usuario=self.request.user)

    def get(self, request, *args, **kwargs):
        """Sobrescreve o comportamento padrão para redirecionar à lista com um parâmetro de confirmação de exclusão."""
        return redirect(reverse('lista') + '?delete=' + str(kwargs['pk']))


class CapsulaDetail(LoginRequiredMixin, DetailView):
    """Exibe os detalhes e o conteúdo de uma cápsula específica."""
    model = Capsula
    template_name = 'capsula_detail.html'
    context_object_name = 'capsula'

    def get_queryset(self):
        """Filtra o acesso para que apenas o dono da cápsula visualize os detalhes."""
        return Capsula.objects.filter(usuario=self.request.user)


class AutorizarEdicaoView(LoginRequiredMixin, CapsulaEditMixin, View):
    """Processa a tentativa de acesso à edição de uma cápsula protegida."""
    def post(self, request, pk):
        """Valida a senha e se a cápsula pode ou não ser editada. Em caso de sucesso, autoriza a sessão do usuário para edição."""
        capsula = self.get_capsula(pk)

        if not capsula.pode_ser_editada():
            return redirect('lista')

        senha = request.POST.get('senha', '')

        if capsula.check_senha(senha):
            self.authorize_edit_session(capsula)
            return redirect(reverse('lista') + f'?edit_form={pk}')

        return redirect(reverse('lista') + f'?edit={pk}&wrong=1')


class EditarCapsulaView(LoginRequiredMixin, CapsulaEditMixin, View):
    """Executa a alteração efetiva dos dados da cápsula e do texto associado."""
    def post(self, request, itemtexto_pk):
        """Verifica a autorização na sessão, valida o formulário de edição e limpa a sessão após o sucesso."""
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
