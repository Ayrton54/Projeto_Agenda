from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'acountts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario,
                             password=senha)
    if not user:
        messages.error(request, 'usuario ou senha invalido.')
        return render(request, 'acountts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'acountts/register.html')

    nome = request.POST.get('nome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    sobrenome = request.POST.get('sobrenome')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario \
            or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode fica vazio')
        return render(request, 'acountts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'EMAIL INVALIDO')
        return render(request, 'acountts/register.html')

    if len(senha) < 6:
        messages.error(request, 'senha curta, precisa ter mais de 6 caracteres')
        return render(request, 'acountts/register.html')
    if len(usuario) < 6:
        messages.error(request, 'usario precisa ter mais de 6 caracteres')
        return render(request, 'acountts/register.html')
    if senha != senha2:
        messages.error(request, 'A senha tem que ser iguais')
        return render(request, 'acountts/register.html')
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario já existe.')
        return render(request, 'acountts/register.html')
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe.')
        return render(request, 'acountts/register.html')
    messages.success(request, 'Registrado com sucesso!'
                              'faça seu login')
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'acountts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar o formulário.')
        form = FormContato(request.POST)
        return render(request, 'acountts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'acountts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')
