from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class Disciplina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disciplinas', verbose_name="Usuário")
    nome = models.CharField(max_length=100, unique=False, verbose_name="Nome da Disciplina")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    codigo = models.CharField(max_length=20, unique=False, verbose_name="Código da Disciplina")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class DiaSemana(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class CronogramaDisciplina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cronogramas', verbose_name="Usuário")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='cronogramas_disciplina', verbose_name="Disciplina")
    carga_horaria = models.IntegerField(verbose_name="Horas de Estudo por Semana")
    dias_da_semana = models.ManyToManyField(DiaSemana, verbose_name="Dias de Estudo")
    
    last_reviewed = models.DateField(default=timezone.now, verbose_name="Última Revisão")
    next_review = models.DateField(default=timezone.now, verbose_name="Próxima Revisão")
    interval_days = models.IntegerField(default=0, verbose_name="Intervalo (dias)")
    ease_factor = models.DecimalField(max_digits=5, decimal_places=2, default=2.5, verbose_name="Fator de Facilidade (EF)")
    review_count = models.IntegerField(default=0, verbose_name="Contagem de Revisões")

    def calculate_next_review(self, quality_of_recall):
        if quality_of_recall >= 3:
            self.ease_factor += (Decimal('0.1') - Decimal(str(5 - quality_of_recall)) * (Decimal('0.08') + Decimal(str(5 - quality_of_recall)) * Decimal('0.02')))
        else:
            self.ease_factor -= Decimal('0.20')
        
        if self.ease_factor < 1.3:
            self.ease_factor = 1.3
        
        if quality_of_recall < 3:
            self.interval_days = 1
        elif self.review_count == 0:
            self.interval_days = 1
        elif self.review_count == 1:
            self.interval_days = 6
        else:
            self.interval_days = round(self.interval_days * float(self.ease_factor))
        
        if quality_of_recall >= 3:
            self.review_count += 1
        else:
            self.review_count = 0

        self.last_reviewed = timezone.now().date()
        self.next_review = self.last_reviewed + timedelta(days=self.interval_days)
        
        self.save()

    def __str__(self):
        return f"Cronograma de {self.disciplina.nome} (Próx. Revisão: {self.next_review})"

    class Meta:
        verbose_name = "Cronograma da Disciplina (Estudo Espaçado)"
        verbose_name_plural = "Cronogramas das Disciplinas (Estudo Espaçado)"
        ordering = ['next_review']
        unique_together = ('user', 'disciplina')

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome