# projetoPA/disciplinas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('listar/', views.listar_disciplinas, name='listar_disciplinas'),
    path('editar/<int:pk>/', views.editar_disciplina, name='editar_disciplina'),
    path('deletar/<int:pk>/', views.deletar_disciplina, name='deletar_disciplina'),
]