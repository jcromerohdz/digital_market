from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

from models import Producto

# Create your views here.

def home(request):
    #Logico de negocio alias hechizo
    m = "Hello Django!!!!"
    contexto= {"mensaje":m}
    return render(request, 'home.html', contexto)

def lista_productos(request):
    #Logico de negocio alias hechizo
    productos = Producto.objects.all()
    print request
    m = "productos nuevo"
    template = "productos.html"
    contexto= {"mensaje":m,
               "productos": productos }
    return render(request, template, contexto)

def detalle(request, object_id=None):
    #Logico de negocio alias hechizo
    # producto = get_object_or_404(Produto, id=object_id)
    # m = "productos nuevo"
    # template = "detalle.html"
    # contexto= {"mensaje":m,
    #        "producto": producto }
    # return render(request, template, contexto)

    if object_id is not None:
        try:
            producto = Producto.objects.get(id=object_id)
            m = "productos nuevo"
            template = "detalle.html"
            contexto= {"mensaje":m,
                   "producto": producto }
            return render(request, template, contexto)
        except Producto.DoesNotExist:
            producto = None
            m = "productos nuevo"
            template = "detalle.html"
            contexto= {"mensaje":m,
                   "producto": producto }
            return render(request, template, contexto)
