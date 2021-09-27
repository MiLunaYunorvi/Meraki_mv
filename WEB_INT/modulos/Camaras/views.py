from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request, 'index.html')

def caja(request):
    return render(request, 'caja.html')

def camaras(request):
    return render(request, 'camaras.html')

###################CAMARAS########################
def camara1(request):
    return render(request, 'camara1.html')
def camara2(request):
    return render(request, 'camara2.html')
def camara3(request):
    return render(request, 'camara3.html')
def camara4(request):
    return render(request, 'camara4.html')
def camara5(request):
    return render(request, 'camara5.html')
def camara6(request):
    return render(request, 'camara6.html')
