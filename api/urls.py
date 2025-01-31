from django.urls import path
from .views import otimizar_rota

urlpatterns = [
    path('otimizar_rota/', otimizar_rota, name='otimizar_rota'),
]
