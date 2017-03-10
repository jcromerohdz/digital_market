from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

class Producto(models.Model):
    nombre  = models.CharField(max_length = 40)
    slug  = models.SlugField(blank=True)#unique=True
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9999, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=9999, decimal_places=2,
                                        null=True, blank=True)
    tipo = models.CharField(max_length = 40, blank=True, null=True, default="foto")

    def __unicode__(self):
        return self.nombre

def producto_pre_save_reciever(sender, instance, *args, **kwargs):
    print sender
    print instance

    if not instance.slug:
        instance.slug = slugify(instance.nombre)

pre_save.connect(producto_pre_save_reciever, sender=Producto)
