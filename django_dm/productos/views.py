from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


from .models import Producto
from .forms import ProductoAddForm, ProductosModelForm
# Create your views here.

def home(request):
    #Logico de negocio alias hechizo
    m = "Hello Django!!!!"
    contexto= {"mensaje":m}
    return render(request, 'home.html', contexto)

class ProductoDetailView(DetailView):
    model = Producto

class ProductoListView(ListView):
    model = Producto

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductoListView, self).get_queryset(**kwargs)
        return qs

def lista_productos(request):
    #Logico de negocio alias hechizo
    productos = Producto.objects.all()
    print request
    m = "productos nuevo"
    template = "productos.html"
    contexto= {"mensaje":m,
               "productos": productos }
    return render(request, template, contexto)

def detalle_slug(request, slug=None):
    #Logico de negocio alias hechizo
    print "hola"
    try:
        producto = get_object_or_404(Producto, slug=slug)
    except Producto.MultipleObjectsReturned:
        producto = Producto.objects.filter(slug=slug).order_by("-nombre").first()

    print producto
    m = "productos nuevo"
    template = "detalle.html"
    contexto= {"mensaje":m,
           "producto": producto }
    return render(request, template, contexto)


def detalle_s(request, slug=None):
    #Logico de negocio alias hechizo
    try:
        producto = get_object_or_404(Producto, slug=slug)
    except Producto.MultipleObjectsReturned:
        producto = Producto.objects.filter(slug=slug).order_by("-nombre").first()
    m = "productos nuevo"
    template = "detalle.html"
    contexto= {"mensaje":m,
           "producto": producto }
    return render(request, template, contexto)

def crear_producto(request):
    #FORM
    #form = ProductoAddForm(request.POST or None)
    form = ProductosModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        print "Alta exitosa!"
    # if request.method == "POST":
    #     print request.POST
    # if form.is_valid():
    #     # print request.POST
    #     data = form.cleaned_data
    #     nombre = data.get("nombre")
    #     descripcion = data.get("descripcion")
    #     precio = data.get("precio")
    #     # nuevo_producto = Producto.object.create(nombre = nombre,
    #     #                                         descripcion = descripcion,
    #     #                                         precio = precio)
    #     nuevo_producto = Producto()
    #     nuevo_producto.nombre = nombre
    #     nuevo_producto.descripcion = descripcion
    #     nuevo_producto.precio = precio
    #     nuevo_producto.save()

    template = "crear_producto.html"
    context = {
        "titulo":"Crear Producto!",
        "form":form
    }

    return render(request, template, context)

def actualizar(request, object_id=None):
    #Logico de negocio alias hechizo
    producto = get_object_or_404(Producto, id=object_id)
    form = ProductosModelForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        print "Actualizacion exitosa!"
    template = "actualizar.html"
    contexto= {
           "producto": producto,
           "form":form,
           "titulo":"Actualizar Producto"
           }
    return render(request, template, contexto)



def detalle(request, object_id=None):
    #Logico de negocio alias hechizo
    producto = get_object_or_404(Producto, id=object_id)
    m = "productos nuevo"
    template = "detalle.html"
    contexto= {"mensaje":m,
           "producto": producto }
    return render(request, template, contexto)

    # if object_id is not None:
    #     try:
    #         producto = Producto.objects.get(id=object_id)
    #         m = "productos nuevo"
    #         template = "detalle.html"
    #         contexto= {"mensaje":m,
    #                "producto": producto }
    #         return render(request, template, contexto)
    #     except Producto.DoesNotExist:
    #         producto = None
    #         m = "productos nuevo"
    #         template = "detalle.html"
    #         contexto= {"mensaje":m,
    #                "producto": producto }
    #         return render(request, template, contexto)
