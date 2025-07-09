# projetoPA/disciplinas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('listar/', views.listar_disciplinas, name='listar_disciplinas'),
    path('editar/<int:pk>/', views.editar_disciplina, name='editar_disciplina'),
    path('deletar/<int:pk>/', views.deletar_disciplina, name='deletar_disciplina'),
    path('cronogramas/', views.listar_cronogramas, name='listar_cronogramas'),
    path('cronogramas/criar/', views.criar_cronograma, name='criar_cronograma'),
    path('cronogramas/editar/<int:pk>/', views.editar_cronograma, name='editar_cronograma'),
    path('cronogramas/deletar/<int:pk>/', views.deletar_cronograma, name='deletar_cronograma'),
]
