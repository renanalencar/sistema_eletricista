from django.shortcuts import render

# Create your views here.
def BuscaCliente(request):
    q = request.GET.get('BuscaCliente')
    if q is not None:
        resultCliente = Cliente.objects.BuscarCliente(q)
    return render(request, 'busca_cliente.html', {'resultcliente': resultCliente})
    