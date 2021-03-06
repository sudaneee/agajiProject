from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from api import consumer

ws_pattern= [
    path('ws/reports/',consumer.Reports.as_asgi()),
    path('ws/safetrip/',consumer.SafeTrip.as_asgi()),

]

application= ProtocolTypeRouter(
    {
        'websocket':AuthMiddlewareStack(URLRouter(ws_pattern))
    }
)