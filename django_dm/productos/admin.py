from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.

from productos.models import Producto, MisProductos



class ProductoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "descripcion", "precio", "precio_oferta"]
    search_fields = ["nombre", "descripcion"]
    list_editable = ["precio_oferta"]
    list_filter = ["precio"]
    class Meta:
        model = Producto

admin.site.register(Producto, ProductoAdmin)

admin.site.register(MisProductos)
