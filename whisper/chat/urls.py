from django.urls import re_path
from .views import chatPage, userSearch, userChats

urlpatterns = [
    re_path(r'^chat/(?P<room_name>[^/]+)', chatPage, name='chatPage'),  # Captures any string as room_name
    re_path('search', userSearch, name='userSearch'),
    re_path('userchats', userChats, name='userSearch')
]