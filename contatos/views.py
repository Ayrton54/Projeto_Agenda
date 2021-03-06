from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from .models import Contato
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html',
                  {'contatos': contatos

                   })


def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    # if not contato.mostrar:
    #     raise Http404()
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')
    if termo is None or not termo:
        messages.add_message(request,
                             messages.ERROR, 'campo PESQUISA não pode fica vazio')
        return redirect('index')
    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    paginator = Paginator(contatos, 4)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html',
                  {'contatos': contatos

                   })
