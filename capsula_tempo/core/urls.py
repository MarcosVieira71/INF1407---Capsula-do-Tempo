from django.urls import path

from core.views import ListaCapsulas, DeletarCapsula, CriarCapsula, CapsulaDetail, UsuarioLoginView, UsuarioLogoutView, UsuarioCriaView, UsuarioAtualizaView, HomeView, UsuarioPasswordResetView, UsuarioPasswordResetDoneView, UsuarioPasswordResetConfirmView, UsuarioPasswordResetCompleteView

urlpatterns = [
    path('', ListaCapsulas.as_view(), name='lista'),
    path('deletar/<int:pk>/', DeletarCapsula.as_view(), name='deletar'),
    path('nova/', CriarCapsula.as_view(), name='criar'),
    path('capsula/<int:pk>/', CapsulaDetail.as_view(), name='detalhe'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('registro/', UsuarioCriaView.as_view(), name='registro'),
    path('perfil/', UsuarioAtualizaView.as_view(), name='perfil'),
    path('home/', HomeView.as_view(), name='home'),
    path('password_reset/', UsuarioPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UsuarioPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UsuarioPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UsuarioPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
