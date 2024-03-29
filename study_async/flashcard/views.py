from django.shortcuts import render,redirect
from .models import Categoria,Flashcard,Desafio,FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages
# Create your views here.
def novo_flashcard(request):


    if request.method == 'GET':
        categoria = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards=Flashcard.objects.filter(user=request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

        return render(request,'novo_flashcard.html',{'categoria': categoria, 'dificuldades': dificuldades,'flashcards': flashcards})
    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip())==0 or  len(resposta.strip()) ==0:
            messages.add_message(request,constants.ERROR,"preencha os campos de pergunta e resposta")
            return redirect('/flashcard/novo_flashcard/')
        flashcard=Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )
        flashcard.save()
        messages.add_message(request,constants.SUCCESS,"reposta adicionada")
        return redirect('/flashcard/novo_flashcard/')
def deletar_flashcard(request, id):
    #aumentar a segurança
    flashcard = Flashcard.objects.get(id=id)
    flashcard.delete()
    messages.add_message(request, constants.SUCCESS, "flashcard excluido")
    return redirect('/flashcard/novo_flashcard/')  # Adicionado 'return' aqui
def iniciar_desafio(request):
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    if request.method == "GET":
        return render(request,'iniciar_desafio.html',{'categorias':categorias, 'dificuldades':dificuldades})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(user=request.user,titulo=titulo,quantidade_perguntas=qtd_perguntas,dificuldade=dificuldade)
        desafio.save()
        desafio.categoria.add(*categorias)
        flashcard = Flashcard.objects.filter(user = request.user).filter(dificuldade=dificuldade).filter(categoria_id__in=categorias).order_by('?')
        #se tiver menos flahcard como validar
        if flashcard.count < int(qtd_perguntas):
            return redirect('flashcard/iniciar_desafio/')
        flashcard=flashcard[: int(qtd_perguntas)]
        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()

        return redirect(f'/flashcard/desafio/{desafio.id}')