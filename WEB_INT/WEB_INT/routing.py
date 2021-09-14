from channels.auth import AuhMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

application = ProtocolTypeRouter({
    'websocket' : 'g'
})