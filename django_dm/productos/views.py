import os

from django.conf import settings
#from django.core.servers.basehttp import FileWrapper
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

#3ra Unidad
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

#project implementation Q lookups
from django.db.models import Q

from django_dm.multipleSlugs import MultiSlugMixin

from django_dm.mixins import LoginRequiredMixin

from .models import Producto
from .forms import ProductoAddForm, ProductosModelForm
# Create your views here.

def home(request):
    #Logico de negocio alias hechizo
    m = "Hello Django!!!!"
    contexto= {"mensaje":m}
    return render(request, 'home.html', contexto)


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
#   template_name = "form.html"
    form_class = ProductosModelForm
    #success_url = "/producto/crear/"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductoCreateView, self).get_context_data(*args, **kwargs)
        context["submit_btn"]="Guardar"
        return context

    def form_valid(self, form):
        usuario = self.request.user
        form.instance.usuario = usuario
        valid_data = super(ProductoCreateView, self).form_valid(form)
        form.instance.administradores.add(usuario)
        return valid_data

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
#    template_name = "form.html"
    form_class = ProductosModelForm
    #success_url = "/productos/lista/"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductoUpdateView, self).get_context_data(*args, **kwargs)
        context["submit_btn"]="Editar"
        return context

    def get_object(self, *args, **kwargs):
        usuario = self.request.user
        obj = super(ProductoUpdateView, self).get_object(*args, **kwargs)
        if obj.usuario == usuario or usuario in obj.administradores.all():
            return obj
        else:
            return Http404

class ProductoDetailView(MultiSlugMixin, DetailView):
    model = Producto


    #t=MultiSlugMixin
    #Manejar el error de multiples slugs
    # def get_object(self, *args, **kwargs):
    #      print self.kwargs
    #      slug = self.kwargs.get("slug")
    #      print slug
    #      ModelClass = self.model
    #      if slug is not None:
    #          try:
    #              #producto = get_object_or_404(Producto, slug=slug)
    #              obj = get_object_or_404(ModelClass, slug=slug)
    #          except:
    # #             #producto = Producto.objects.filter(slug=slug).order_by("-nombre").first()
    #              obj = ModelClass.objects.filter(slug=slug).order_by("-nombre").first()
    #      else:
    #          obj = super(ProductoDetailView, self).get_object(*args, **kwargs)
    #
    #      return obj

class ProductoDownloadView(MultiSlugMixin, DetailView):
    model = Producto

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.misproductos.productos.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(file(filepath))
            mimetype = 'application/force-download'
            if guessed_type :
                mimetype = guessed_type

            response =  HttpResponse(wrapper, content_type=mimetype )

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)

            response["X-SendFile"] =  str(obj.media.name)
            return response
        else:
            raise Http404



class ProductoListView(ListView):
    model = Producto

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductoListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        #qs = qs.filter(nombre__icontains=query)
        qs =qs.filter(
                      Q(nombre__icontains=query)|
                      Q(descripcion__icontains=query)
                      ).order_by("nombre")
        print query
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
