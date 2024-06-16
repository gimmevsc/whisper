from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chatroom/chat', ChatroomConsumer.as_asgi()),
]   