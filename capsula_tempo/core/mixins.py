from django.shortcuts import get_object_or_404

from .models import Capsula


class CapsulaEditMixin:

    def get_capsula(self, pk):
        return get_object_or_404(Capsula, pk=pk, usuario=self.request.user)

    def _session_key_for(self, capsula):
        return f'capsula_edit_{capsula.pk}'

    def is_edit_session_authorized(self, capsula):
        return bool(self.request.session.get(self._session_key_for(capsula)))

    def authorize_edit_session(self, capsula):
        self.request.session[self._session_key_for(capsula)] = True
        self.request.session.modified = True

    def clear_edit_session(self, capsula):
        self.request.session.pop(self._session_key_for(capsula), None)
