from django.urls import path

from .views import *

urlpatterns = [
    path('reset', enterEmail),
    path('reset/confirmation', resetPassword)
]