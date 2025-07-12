from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm
from .models import UserProfile


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            curso_selecionado = form.cleaned_data.get('curso')
            UserProfile.objects.create(user=user, curso=curso_selecionado)

            login(request, user)
            messages.success(request, 'Conta criada e login efetuado com sucesso!')
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {username}!')
                
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Erro no formulário de login. Por favor, verifique os dados.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect(settings.LOGOUT_REDIRECT_URL) 

@login_required(login_url='accounts:login')
def restricted_page(request):
    return render(request, 'accounts/restricted_page.html')