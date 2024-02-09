# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Gasto
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from app_calculando_gastos.forms import CustomUserCreationForm
from django.contrib.auth import authenticate


def index(request):
    return render(request, 'index.html')

def home(request):
    gastos = Gasto.objects.all()
    total_gasto = sum(gasto.valor for gasto in gastos)

    success_message = request.session.pop('success_message', None)

    context = {'success_message': success_message, 'gastos': gastos, 'total_gasto': total_gasto}
    return render(request, 'home.html', context)


def processar_gastos(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')

        Gasto.objects.create(descricao=descricao, valor=valor)

    # Redirecionar para a página de confirmação após o processamento
    return redirect('confirmacao')

def delete_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, pk=gasto_id)
    gasto.delete()

    # Adicionar a mensagem apenas se não estiver no painel de administração
    if not request.path.startswith('/admin/'):
        messages.success(request, 'Gasto excluído com sucesso.')

    # Redirecionar de volta para a página de onde veio ou para a página inicial
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))

def confirmacao(request):
    gastos = Gasto.objects.all()
    total_gasto = sum(gasto.valor for gasto in gastos)
    return render(request, 'confirmacao.html', {'gastos': gastos, 'total_gasto': total_gasto})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
   

def login_view(request):
    if request.method == 'POST':
        # Lógica de autenticação do usuário
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, 'login.html')