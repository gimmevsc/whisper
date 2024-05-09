from django.urls import path

from .views import *

urlpatterns = [
    path('hui/', index),
    path('hui/<int:catid>/', categories)
]
