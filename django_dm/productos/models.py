from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre  = models.CharField(max_length = 40)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9999, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=9999, decimal_places=2,
                                        null=True, blank=True)

    def __unicode__(self):
        return self.nombre
