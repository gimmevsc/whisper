"""
ASGI config for whisper project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
# from chat.routing import websocket_urlpatterns
import os
from channels.layers import get_channel_layer
from chat.consumers import PersonalChatConsumer
from django.urls import re_path

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whisper.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/chat/(?P<user_id>\w+)', PersonalChatConsumer.as_asgi())
                # re_path(r'ws/onlinef', OnlineStatusConsumer.as_asgi())
                # re_path('ws/online/', OnlineStatusConsumer.as_asgi())
                # websocket_urlpatterns
            ])
        ),
    }
)
channel_layer = get_channel_layer()