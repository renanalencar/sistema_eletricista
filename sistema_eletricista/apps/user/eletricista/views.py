from django.shortcuts import render

# Create your views here.
def BuscaEletricista(request):
    q = request.GET.get('buscaEletricista')
    if q is not None:
        resultEletricista = Eletricista.objects.BuscarEletricista(q)
    return render(request, 'busca_eletricista.html', {'resultEletricista': resultEletricista})