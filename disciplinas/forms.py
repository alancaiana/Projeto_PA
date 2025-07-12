from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from disciplinas.models import Disciplina, CronogramaDisciplina, Curso, DiaSemana
from accounts.models import UserProfile

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'descricao', 'codigo', 'ativa']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class CronogramaDisciplinaForm(forms.ModelForm):
    disciplina = forms.ModelChoiceField(
        queryset=Disciplina.objects.filter(ativa=True).order_by('nome'),
        label="Selecione a Disciplina",
        empty_label="--- Escolha uma Disciplina ---"
    )

    dias_da_semana = forms.ModelMultipleChoiceField(
        queryset=DiaSemana.objects.all().order_by('id'),
        widget=forms.CheckboxSelectMultiple,
        label="Dias de Estudo",
        help_text="Marque os dias em que você planeja estudar esta disciplina."
    )

    class Meta:
        model = CronogramaDisciplina
        fields = ['disciplina', 'carga_horaria', 'dias_da_semana']
        labels = {
            'carga_horaria': 'Horas de Estudo por Semana',
        }
        help_texts = {
            'carga_horaria': 'Informe a quantidade de horas que você dedicará a esta disciplina por semana.',
        }
        widgets = {
            'carga_horaria': forms.NumberInput(attrs={'placeholder': 'Ex: 5 (horas por semana)'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['disciplina'].queryset = Disciplina.objects.filter(user=user, ativa=True).order_by('nome')

class CustomUserCreationForm(UserCreationForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('nome'),
        empty_label="Selecione seu curso",
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'curso')