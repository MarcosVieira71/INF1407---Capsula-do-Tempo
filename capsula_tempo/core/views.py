from .views_capsula import (
    ListaCapsulas,
    CriarCapsula,
    DeletarCapsula,
    CapsulaDetail,
    AutorizarEdicaoView,
    EditarCapsulaView,
)

from .views_auth import (
    UsuarioLoginView,
    UsuarioLogoutView,
    UsuarioCriaView,
    UsuarioAtualizaView,
    UsuarioAtualizaSenhaView,
    UsuarioExcluirView,
    HomeView,
    UsuarioPasswordResetView,
    UsuarioPasswordResetDoneView,
    UsuarioPasswordResetConfirmView,
    UsuarioPasswordResetCompleteView,
)

__all__ = [
    'ListaCapsulas',
    'CriarCapsula',
    'DeletarCapsula',
    'CapsulaDetail',
    'AutorizarEdicaoView',
    'EditarCapsulaView',
    'UsuarioLoginView',
    'UsuarioLogoutView',
    'UsuarioCriaView',
    'UsuarioAtualizaView',
    'UsuarioAtualizaSenhaView',
    'UsuarioExcluirView',
    'HomeView',
    'UsuarioPasswordResetView',
    'UsuarioPasswordResetDoneView',
    'UsuarioPasswordResetConfirmView',
    'UsuarioPasswordResetCompleteView',
]