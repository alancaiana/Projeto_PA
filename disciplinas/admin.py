from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Disciplina, CronogramaDisciplina, Curso, DiaSemana 

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'ativa', 'link_para_minha_aba_html')

    def link_para_minha_aba_html(self, obj):
        url = reverse('listar_disciplinas')
        return format_html('<a href="{}" target="_blank">Ver na Minha Plataforma</a>', url)

    link_para_minha_aba_html.short_description = 'Ação Customizada'

@admin.register(CronogramaDisciplina)
class CronogramaDisciplinaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'carga_horaria', 'exibir_dias_da_semana', 'last_reviewed', 'next_review', 'review_count')
    list_filter = ('disciplina', 'dias_da_semana') 
    search_fields = ('disciplina__nome', 'dias_da_semana__nome') 

    def exibir_dias_da_semana(self, obj):
        return ", ".join([dia.nome for dia in obj.dias_da_semana.all()])

    exibir_dias_da_semana.short_description = 'Dias de Estudo' 

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(DiaSemana)
class DiaSemanaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)