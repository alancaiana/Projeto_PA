from django.shortcuts import render, redirect, get_object_or_404
from .forms import DisciplinaForm 
from .models import Disciplina, CronogramaDisciplina 
from .forms import CronogramaDisciplinaForm
from accounts.forms import CustomAuthenticationForm

def home(request):
    form = CustomAuthenticationForm() # Cria uma instância do formulário de login
    return render(request, 'disciplinas/home.html', {'form': form}) # Passa o formulário para o template

def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas') 
    else:
        form = DisciplinaForm()
    return render(request, 'disciplinas/cadastrar_disciplina.html', {'form': form})

def listar_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplinas/listar_disciplinas.html', {'disciplinas': disciplinas})

def editar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'disciplinas/editar_disciplina.html', {'form': form, 'disciplina': disciplina})

def deletar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        disciplina.delete()
        return redirect('listar_disciplinas')
    return render(request, 'disciplinas/confirmar_deletar_disciplina.html', {'disciplina': disciplina})

def home(request):
    return render(request, 'disciplinas/home.html')

def listar_cronogramas(request):
    # Puxa todos os cronogramas existentes, ordenados pelo nome da disciplina
    cronogramas = CronogramaDisciplina.objects.all().order_by('disciplina__nome')
    return render(request, 'disciplinas/cronograma_listar.html', {'cronogramas': cronogramas})

def criar_cronograma(request):
    if request.method == 'POST':
        form = CronogramaDisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cronogramas') # Redireciona para a lista após criar
    else:
        form = CronogramaDisciplinaForm()
    return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Criar'})

def editar_cronograma(request, pk):
    cronograma = get_object_or_404(CronogramaDisciplina, pk=pk)
    if request.method == 'POST':
        form = CronogramaDisciplinaForm(request.POST, instance=cronograma)
        if form.is_valid():
            form.save()
            return redirect('listar_cronogramas') # Redireciona para a lista após editar
    else:
        form = CronogramaDisciplinaForm(instance=cronograma)
    return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Editar', 'cronograma': cronograma})

def deletar_cronograma(request, pk):
    cronograma = get_object_or_404(CronogramaDisciplina, pk=pk)
    if request.method == 'POST':
        cronograma.delete()
        return redirect('listar_cronogramas') # Redireciona para a lista após deletar
    return render(request, 'disciplinas/cronograma_confirmar_deletar.html', {'cronograma': cronograma})