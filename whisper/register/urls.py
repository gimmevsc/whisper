from django.urls import path

from .views import *

urlpatterns = [
    path('register', registerUser),
    path('hui/<int:catid>/', categories)
]
