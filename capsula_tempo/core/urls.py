from django.urls import path

from core.views import ListaCapsulas, DeletarCapsula, CriarCapsula, CapsulaDetail

urlpatterns = [
    path('', ListaCapsulas.as_view(), name='lista'),
    path('deletar/<int:pk>/', DeletarCapsula.as_view(), name='deletar'),
    path('nova/', CriarCapsula.as_view(), name='criar'),
    path('capsula/<int:pk>/', CapsulaDetail.as_view(), name='detalhe'),
]
