from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from disciplinas.models import Curso
from .models import UserProfile 

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomUserCreationForm(UserCreationForm):

    nome_completo = forms.CharField(
        max_length=255, 
        required=False, 
        label="Nome Completo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    matricula = forms.CharField(
        max_length=50,
        required=False, 
        label="Matrícula",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('nome'),
        empty_label="Selecione seu curso",
        label="Curso",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'nome_completo', 'matricula', 'curso') 

    def save(self, commit=True):
        user = super().save(commit=True) 

        nome_completo = self.cleaned_data.get('nome_completo')
        matricula = self.cleaned_data.get('matricula')
        curso_selecionado = self.cleaned_data.get('curso')

        profile = UserProfile(
            user=user,
            nome_completo=nome_completo,
            matricula=matricula,
            curso=curso_selecionado
        )
        if commit:
            profile.save()
        return user