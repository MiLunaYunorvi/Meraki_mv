from .views import camara1
from modulos.Camaras.views import index
from django.urls import path

urlpatterns = [
    path('',camara1,name='camara1'),
    #path('camara1.html/',camara1, name='camara1'),
]
