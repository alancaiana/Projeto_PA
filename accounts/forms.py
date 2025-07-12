from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from disciplinas.models import Curso

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) 

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('nome'), 
        empty_label="Selecione seu curso", 
        label="Curso", 
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('curso',)