from django.urls import re_path
from .views import chatPage

urlpatterns = [
    re_path(r'^chat/(?P<room_name>[^/]+)', chatPage, name='chatPage'),  # Captures any string as room_name
]