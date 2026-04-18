from django.urls import path

from core.views import ListaCapsulas, DeletarCapsula, CriarCapsula, CapsulaDetail, UsuarioLoginView, UsuarioLogoutView, UsuarioCriaView, UsuarioAtualizaView, HomeView

urlpatterns = [
    path('', ListaCapsulas.as_view(), name='lista'),
    path('deletar/<int:pk>/', DeletarCapsula.as_view(), name='deletar'),
    path('nova/', CriarCapsula.as_view(), name='criar'),
    path('capsula/<int:pk>/', CapsulaDetail.as_view(), name='detalhe'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('registro/', UsuarioCriaView.as_view(), name='registro'),
    path('perfil/', UsuarioAtualizaView.as_view(), name='perfil'),
    path('', HomeView.as_view(), name='home')
]
