# projetoPA/disciplinas/forms.py

from django import forms
from .models import Disciplina, CronogramaDisciplina 

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'descricao', 'codigo', 'ativa']
        widgets = {
            'Descrição': forms.Textarea(attrs={'rows': 4}),
        }

class CronogramaDisciplinaForm(forms.ModelForm):
    class Meta:
        model = CronogramaDisciplina
        fields = ['disciplina', 'carga_horaria', 'dias_da_semana']
        widgets = {
            'carga_horaria': forms.TextInput(attrs={'placeholder': 'Ex: 6 h'}),
            'dias_da_semana': forms.TextInput(attrs={'placeholder': 'Ex: Segunda-feira, Quarta-feira'})
        }