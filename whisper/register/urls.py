from django.urls import path

from .views import *

urlpatterns = [
    path('register', registerUser),
    path('register/confirmation', emailConfirmation),
    path('register/confirmation/resend', resendConfirmationCode)
]