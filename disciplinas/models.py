# projetoPA/disciplinas/models.py

from django.db import models

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Disciplina")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código da Disciplina")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome'] # Ordena as disciplinas pelo nome por padrão

    def __str__(self):
        return self.nome