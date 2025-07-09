# projetoPA/disciplinas/forms.py

from django import forms
from .models import Disciplina

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'descricao', 'codigo', 'ativa']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }