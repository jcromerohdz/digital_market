from django.contrib import admin

# Register your models here.

from productos.models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "descripcion", "precio", "precio_oferta"]
    search_fields = ["nombre", "descripcion"]
    list_editable = ["precio_oferta"]
    list_filter = ["precio"]
    class Meta:
        model = Producto

admin.site.register(Producto, ProductoAdmin)
