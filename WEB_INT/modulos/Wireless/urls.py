from .views import wireless
from modulos.Camaras.views import index
from django.urls import path


urlpatterns = [
    path('',wireless,name='wireless'),
    #path('camara1.html/',camara1, name='camara1'),
]
