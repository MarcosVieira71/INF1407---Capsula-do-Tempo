"""
Módulo de Mixins para controle de permissões e sessões de edição.

Este módulo fornece utilitários para verificar se um usuário possui autorização
temporária (via sessão) para modificar o conteúdo de uma cápsula protegida.
"""

from django.shortcuts import get_object_or_404

from .models import Capsula


class CapsulaEditMixin:
    """
    Mixin para gerenciar a autorização de edição de cápsulas baseada em sessão.
    
    Fornece métodos para validar o proprietário da cápsula e gerenciar flags
    temporárias na sessão que permitem a edição após a validação de senha.
    """

    def get_capsula(self, pk):
        """
        Recupera uma cápsula específica garantindo que pertença ao usuário logado.

        Args:
            pk (int): Chave primária da cápsula.

        Returns:
            Capsula: Instância da cápsula encontrada.

        Raises:
            Http404: Caso a cápsula não exista ou não pertença ao usuário.
        """
        return get_object_or_404(Capsula, pk=pk, usuario=self.request.user)

    def _session_key_for(self, capsula):
        """Gera uma chave de sessão única para a autorização de uma cápsula específica."""
        return f'capsula_edit_{capsula.pk}'

    def is_edit_session_authorized(self, capsula):
        """Verifica se a sessão atual possui autorização para editar a cápsula informada."""
        return bool(self.request.session.get(self._session_key_for(capsula)))

    def authorize_edit_session(self, capsula):
        """Marca na sessão que o usuário está autorizado a editar a cápsula informada."""
        self.request.session[self._session_key_for(capsula)] = True
        self.request.session.modified = True

    def clear_edit_session(self, capsula):
        """Remove a autorização de edição da cápsula da sessão atual."""
        self.request.session.pop(self._session_key_for(capsula), None)
