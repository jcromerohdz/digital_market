from django import forms

from .models import Producto
from django.utils.text import slugify

OPCIONES_TIPO = (
    ('foto', "Foto"),
    ('video juego', "Video Juego"),
    ('libro', "Libro"),
)
class ProductoAddForm(forms.Form):
    nombre = forms.CharField(label="Cual es nombre del producto",
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Ponga el nombre'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    precio = forms.DecimalField()
    tipo = forms.ChoiceField(choices=OPCIONES_TIPO)

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio <= 100.00:
            raise forms.ValidationError("El precio debe ser mayor que $100.00")
        elif precio >= 19999.00:
            raise forms.ValidationError("El precio debe ser menos que $19999.00")
        else:
            return precio


class ProductosModelForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=OPCIONES_TIPO)
    class Meta:
        model = Producto
        fields =[
            "nombre",
            "descripcion",
            "precio",
            "tipo"
        ]
        labels = {
            "nombre": "Cual es nombre del producto",
            "descripcion":"Cual es la descripcion",
            "precio":"Cual es precio del producto"
        }
        widgets = {
            "nombre": forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Ponga el nombre'}),
            "descripcion": forms.Textarea(attrs={'class': 'form-control'}),
            "precio": forms.NumberInput(attrs={'class': 'form-control'}),

        }

    def clean(self, *args, **kwargs):
        clean_data = super(ProductosModelForm, self).clean(*args, **kwargs)
        print clean_data
        # nombre = clean_data.get("nombre")
        # slug = slugify(nombre)
        # qs = Producto.objects.filter(slug=slug).exists()
        # if qs:
        #     raise forms.ValidationError("Ese nombre ya existe!, de uno nuevo!. Por favor intente de nuevo.")
        # return clean_data

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio <= 100.00:
            raise forms.ValidationError("El precio debe ser mayor que $100.00")
        elif precio >= 19999.00:
            raise forms.ValidationError("El precio debe ser menos que $19999.00")
        else:
            return precio
