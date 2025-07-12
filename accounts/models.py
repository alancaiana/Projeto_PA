from django.db import models
from django.contrib.auth.models import User
from disciplinas.models import Curso

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    nome_completo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome Completo") # NOVO CAMPO
    matricula = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Matrícula") # NOVO CAMPO
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Curso")

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"