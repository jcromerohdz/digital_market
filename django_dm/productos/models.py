from __future__ import unicode_literals

from django.conf import settings

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


def download_media_location(isinstance, nombre_archivo):
    return "%s/%s" %(isinstance.id, nombre_archivo)

class Producto(models.Model):
    #usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    administradores = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='administradores_producto',
                                             blank=True)#related_name=administradores_producto
    media = models.FileField(blank=True, null=True,
                             upload_to=download_media_location,
                             storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    nombre  = models.CharField(max_length = 40)
    slug  = models.SlugField(blank=True, unique=True)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9999, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=9999, decimal_places=2,
                                        null=True, blank=True)
    tipo = models.CharField(max_length = 40, blank=True, null=True, default="foto")

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        print "URL absoluto"
        view_name = "productos:detalle_slug"
        return reverse(view_name, args=[str(self.slug)])

    def get_download(self):
        view_name = "productos:download_slug"
        url = reverse(view_name, args=[str(self.slug)])
        return url


def create_slug(instance, nuevo_slug=None):
    slug = slugify(instance.nombre)
    if nuevo_slug is not None:
        slug = nuevo_slug

    qs = Producto.objects.filter(slug=slug)
    existe = qs.exists()
    if existe:
        nuevo_slug = "%s-%s" %(slug, qs.last().id)
        return create_slug(instance, nuevo_slug=nuevo_slug)

    return slug

def producto_pre_save_reciever(sender, instance, *args, **kwargs):
    print sender
    print instance

    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(producto_pre_save_reciever, sender=Producto)


class MisProductos(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    productos = models.ManyToManyField(Producto, blank=True)

    def __unicode__(self):
        return "%s" %(self.productos.count())

    class Meta:
        verbose_name = "Mis Productos"
        verbose_name_plural = "Mis Productos"
