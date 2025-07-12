from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Disciplina")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código da Disciplina")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']

    def __str__(self):
        return self.nome

from django.db import models

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class CronogramaDisciplina(models.Model):
    disciplina = models.OneToOneField(Disciplina, on_delete=models.CASCADE, related_name='cronograma')
    carga_horaria = models.CharField(max_length=50) 
    dias_da_semana = models.CharField(max_length=200)

    def __str__(self):
        return f"Cronograma de {self.disciplina.nome}"

    class Meta:
        verbose_name = "Cronograma da Disciplina"
        verbose_name_plural = "Cronogramas das Disciplinas"
        ordering = ['disciplina__nome']

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome