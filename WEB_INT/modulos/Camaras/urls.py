from .views import index,caja,camaras
from .views import camara1,camara2,camara3,camara4,camara5,camara6
from django.urls import path

urlpatterns = [
    #path('',index,name='index'),
    path('',camaras, name='camaras'),
    path('caja/', caja, name='caja'),
    path('camara1/', camara1, name='camara1'),
    path('camara2/', camara2, name='camara2'),
    path('camara3/', camara3, name='camara3'),
    path('camara4/', camara4, name='camara4'),
    path('camara5/', camara5, name='camara5'),
    path('camara6/', camara6, name='camara6'),
    
]