# projetoPA/disciplinas/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import DisciplinaForm
from .models import Disciplina

def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas') # Redireciona para a lista após o cadastro
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