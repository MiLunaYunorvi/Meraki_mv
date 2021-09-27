from django.shortcuts import render

# Create your views here.

def wireless(request):
    return render(request, 'wireless.html')