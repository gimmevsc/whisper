from django.urls import re_path
from .views import chatPage

urlpatterns = [
    re_path('chat/<str:room_name>', chatPage, name='chatPage')
]