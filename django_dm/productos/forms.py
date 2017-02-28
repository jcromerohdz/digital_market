from django import forms


class ProductoAddForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField()
    precio = forms.DecimalField()

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio <= 100.00:
            raise forms.ValidationError("El precio debe ser mayor que $100.00")
        elif precio >= 19999.00:
            raise forms.ValidationError("El precio debe ser menos que $19999.00")
        else:
            raise precio
