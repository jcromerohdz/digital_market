from django.shortcuts import render

# Create your views here.

def home(request):
    #Logico de negocio alias hechizo
    m = "Hello Django!!!!"
    contexto= {"mensaje":m}
    return render(request, 'home.html', contexto)
