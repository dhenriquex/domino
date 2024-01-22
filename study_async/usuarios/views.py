from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "senha e confirmar senha invalido")
            return redirect('/usuarios/cadastro')
        user = User.objects.filter(username=username)  # Corrigido aqui
        if user.exists():
            messages.add_message(request, constants.ERROR, "usuario ja existe")
            return redirect('/usuarios/cadastro')
        try:
            User.objects.create_user(
                username=username,
                password=senha,
            )
            return redirect('/usuarios/logar')
        except:
            messages.add_message(request, constants.ERROR, "erro no servidor")
            return redirect('/usuarios/cadastro')
def logar(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')  # Corrigido aqui
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=senha)  # Corrigido aqui
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'logado')
            return redirect('/flashcard/novo_flashcard')
        else:
            messages.add_message(request, constants.ERROR, 'user ou senha incorreto')
            return redirect('/usuarios/logar')

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')
