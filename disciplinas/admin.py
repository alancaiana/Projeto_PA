from django.contrib import admin
from django.urls import reverse 
from django.utils.html import format_html 
from .models import Disciplina, CronogramaDisciplina, Curso


class DisciplinaAdmin(admin.ModelAdmin):

    list_display = ('nome', 'codigo', 'ativa', 'link_para_minha_aba_html')

    def link_para_minha_aba_html(self, obj):
        url = reverse('listar_disciplinas')
        return format_html('<a href="{}" target="_blank">Ver na Minha Plataforma</a>', url)

    link_para_minha_aba_html.short_description = 'Ação Customizada' 

admin.site.register(Disciplina, DisciplinaAdmin)

@admin.register(CronogramaDisciplina)
class CronogramaDisciplinaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'carga_horaria', 'dias_da_semana')
    list_filter = ('disciplina',)
    search_fields = ('disciplina__nome', 'dias_da_semana') 

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)