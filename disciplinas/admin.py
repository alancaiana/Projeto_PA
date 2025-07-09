# C:\Users\Alan\Documents\Estudos\projetoPA\disciplinas\admin.py

from django.contrib import admin
from django.urls import reverse # Importa reverse para gerar URLs
from django.utils.html import format_html # Importa para formatar HTML
from .models import Disciplina

# Crie uma classe de admin para personalizar o modelo Disciplina
class DisciplinaAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de disciplinas no admin
    list_display = ('nome', 'codigo', 'ativa', 'link_para_minha_aba_html')

    # Cria uma coluna customizada para o link
    def link_para_minha_aba_html(self, obj):
        # Gera a URL para sua view 'listar_disciplinas'
        url = reverse('listar_disciplinas')
        # Retorna o HTML do link. target="_blank" abre em nova aba.
        return format_html('<a href="{}" target="_blank">Ver na Minha Plataforma</a>', url)

    link_para_minha_aba_html.short_description = 'Ação Customizada' # Nome da coluna no admin

admin.site.register(Disciplina, DisciplinaAdmin)