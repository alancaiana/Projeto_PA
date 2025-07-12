from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .forms import DisciplinaForm, CronogramaDisciplinaForm
from .models import Disciplina, CronogramaDisciplina, Curso, DiaSemana
from accounts.forms import CustomAuthenticationForm
from accounts.forms import CustomUserCreationForm
from accounts.models import UserProfile


@login_required(login_url='accounts:login')
def minha_plataforma_inicial(request):
    profile = None
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.warning(request, "Seu perfil não foi totalmente configurado. Atualize suas informações.")
        
    disciplina_count = Disciplina.objects.filter(user=request.user).count()
    cronograma_count = CronogramaDisciplina.objects.filter(user=request.user).count()

    form = CustomAuthenticationForm()

    context = {
        'form': form,
        'profile': profile,
        'disciplina_count': disciplina_count,
        'cronograma_count': cronograma_count,
        'user': request.user,
    }
    return render(request, 'disciplinas/home.html', context)

@login_required(login_url='accounts:login')
def cadastrar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.user = request.user
            disciplina.save()
            messages.success(request, "Disciplina cadastrada com sucesso!")
            return redirect('listar_disciplinas')
        else:
            messages.error(request, "Erro ao cadastrar disciplina. Verifique os dados.")
            return render(request, 'disciplinas/cadastrar_disciplina.html', {'form': form})
    else:
        form = DisciplinaForm()
    return render(request, 'disciplinas/cadastrar_disciplina.html', {'form': form})

@login_required(login_url='accounts:login')
def listar_disciplinas(request):
    disciplinas = Disciplina.objects.filter(user=request.user).order_by('nome')
    return render(request, 'disciplinas/listar_disciplinas.html', {'disciplinas': disciplinas})

@login_required(login_url='accounts:login')
def editar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada com sucesso!")
            return redirect('listar_disciplinas')
        else:
            messages.error(request, "Erro ao atualizar disciplina. Verifique os dados.")
            return render(request, 'disciplinas/editar_disciplina.html', {'form': form, 'disciplina': disciplina})
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'disciplinas/editar_disciplina.html', {'form': form, 'disciplina': disciplina})

@login_required(login_url='accounts:login')
def deletar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk, user=request.user)
    if request.method == 'POST':
        disciplina.delete()
        messages.success(request, "Disciplina excluída com sucesso!")
        return redirect('listar_disciplinas')
    return render(request, 'disciplinas/confirmar_deletar_disciplina.html', {'disciplina': disciplina})

@login_required(login_url='accounts:login')
def listar_cronogramas(request):
    if request.method == 'POST':
        cronograma_id = request.POST.get('cronograma_id')
        quality = int(request.POST.get('quality'))

        cronograma_item = get_object_or_404(CronogramaDisciplina, pk=cronograma_id, user=request.user)
        
        intervalo_anterior = cronograma_item.interval_days 
        
        cronograma_item.calculate_next_review(quality)
        
        dias_adicionados = cronograma_item.interval_days - intervalo_anterior
        
        messages.success(request, f"Revisão de '{cronograma_item.disciplina.nome}' registrada. Próxima revisão em {cronograma_item.interval_days} dias! ({dias_adicionados:+d} dias adicionados)")
        
        return redirect('listar_cronogramas')

    cronogramas = CronogramaDisciplina.objects.filter(user=request.user).order_by('next_review')
    context = {
        'cronogramas': cronogramas,
        'today': timezone.now().date(),
    }
    return render(request, 'disciplinas/cronograma_listar.html', context)

@login_required(login_url='accounts:login')
def criar_cronograma(request):
    if request.method == 'POST':
        form = CronogramaDisciplinaForm(request.POST, user=request.user)
        if form.is_valid():
            disciplina_selecionada = form.cleaned_data['disciplina']
            dias_da_semana_selecionados = form.cleaned_data['dias_da_semana']
            carga_horaria_semanal = form.cleaned_data['carga_horaria']

            existing_cronograma = CronogramaDisciplina.objects.filter(
                user=request.user,
                disciplina=disciplina_selecionada
            ).first()

            if existing_cronograma:
                messages.error(request, f"Cronograma para '{disciplina_selecionada.nome}' já existe. Edite-o ou exclua-o.")
                return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Criar'})

            cronograma = CronogramaDisciplina(
                user=request.user,
                disciplina=disciplina_selecionada,
                carga_horaria=carga_horaria_semanal,
            )

            cronograma.last_reviewed = timezone.now().date()
            cronograma.next_review = timezone.now().date() + timedelta(days=1)
            cronograma.interval_days = 1
            cronograma.review_count = 0
            cronograma.ease_factor = 2.5

            cronograma.save()
            cronograma.dias_da_semana.set(dias_da_semana_selecionados)

            messages.success(request, f"Cronograma para '{disciplina_selecionada.nome}' adicionado com sucesso e primeira revisão agendada para amanhã!")
            return redirect('listar_cronogramas')
        else:
            messages.error(request, "Erro ao criar cronograma. Verifique os dados.")
            return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Criar'})
    else:
        form = CronogramaDisciplinaForm(user=request.user) 
    return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Criar'})


@login_required(login_url='accounts:login')
def editar_cronograma(request, pk):
    cronograma = get_object_or_404(CronogramaDisciplina, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CronogramaDisciplinaForm(request.POST, instance=cronograma, user=request.user)
        if form.is_valid():
            cronograma = form.save(commit=False)
            cronograma.user = request.user
            cronograma.save()
            form.save_m2m()
            messages.success(request, "Cronograma atualizado com sucesso!")
            return redirect('listar_cronogramas')
        else:
            messages.error(request, "Erro ao atualizar cronograma. Verifique os dados.")
            return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Editar', 'cronograma': cronograma})
    else:
        form = CronogramaDisciplinaForm(instance=cronograma, user=request.user)
    return render(request, 'disciplinas/cronograma_form.html', {'form': form, 'acao': 'Editar', 'cronograma': cronograma})


@login_required(login_url='accounts:login')
def deletar_cronograma(request, pk):
    cronograma = get_object_or_404(CronogramaDisciplina, pk=pk, user=request.user)
    if request.method == 'POST':
        cronograma.delete()
        messages.success(request, "Cronograma excluído com sucesso!")
        return redirect('listar_cronogramas')
    return render(request, 'disciplinas/cronograma_confirmar_deletar.html', {'cronograma': cronograma})

@login_required(login_url='accounts:login')
def revisar_disciplinas(request):
    disciplinas_para_revisar = CronogramaDisciplina.objects.filter(
        user=request.user,
        next_review__lte=timezone.now().date()
    ).order_by('next_review', 'disciplina__nome')

    if request.method == 'POST':
        cronograma_id = request.POST.get('cronograma_id')
        quality = int(request.POST.get('quality'))

        cronograma_item = get_object_or_404(CronogramaDisciplina, pk=cronograma_id, user=request.user)
        cronograma_item.calculate_next_review(quality)
        messages.success(request, f"Revisão de '{cronograma_item.disciplina.nome}' registrada. Próxima revisão em {cronograma_item.interval_days} dias!")
        return redirect('revisar_disciplinas')

    return render(request, 'disciplinas/revisar_disciplinas.html', {
        'disciplinas_para_revisar': disciplinas_para_revisar,
        'hoje': timezone.now().date()
    })