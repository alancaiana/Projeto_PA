# C:\Users\Alan\Documents\Estudos\projetoPA\disciplinas\admin.py

from django.contrib import admin
from django.urls import reverse 
from django.utils.html import format_html 
from .models import Disciplina, CronogramaDisciplina # Importe CronogramaDisciplina


class DisciplinaAdmin(admin.ModelAdmin):

    list_display = ('nome', 'codigo', 'ativa', 'link_para_minha_aba_html')

    # Cria uma coluna customizada para o link
    def link_para_minha_aba_html(self, obj):
        # Gera a URL para sua view 'listar_disciplinas'
        url = reverse('listar_disciplinas')
        # Retorna o HTML do link. target="_blank" abre em nova aba.
        return format_html('<a href="{}" target="_blank">Ver na Minha Plataforma</a>', url)

    link_para_minha_aba_html.short_description = 'Ação Customizada' # Nome da coluna no admin

admin.site.register(Disciplina, DisciplinaAdmin)

@admin.register(CronogramaDisciplina)
class CronogramaDisciplinaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'carga_horaria', 'dias_da_semana')
    # Se quiser adicionar um filtro por disciplina:
    list_filter = ('disciplina',)
    search_fields = ('disciplina__nome', 'dias_da_semana') # Permite buscar por nome da disciplina