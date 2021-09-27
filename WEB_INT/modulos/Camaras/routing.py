from django.urls import path
from .consumers import WSConsumer, WSConsumer_cam1,WSConsumer_camaras, WSConsumer_cams_im, WSConsumer_cams_pa

ws_urlpatterns=[
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('ws/camaras/camara1/', WSConsumer_cam1.as_asgi()),
    path('ws/camaras/camara_par/', WSConsumer_cams_pa.as_asgi()),
    path('ws/camaras/camara_im/', WSConsumer_cams_im.as_asgi()),
    path('ws/camaras/', WSConsumer_camaras.as_asgi()),
]

