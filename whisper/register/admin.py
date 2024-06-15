from .models import *
from django.contrib import admin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email_address', 'password', 'phone_number', 'first_name', 'last_name', 'created_at')
    list_display_links = ('user_id', 'username', 'email_address')
    search_fields = ('user_id', 'username', 'email_address', 'password', 'phone_number', 'first_name', 'last_name')
    list_filter = ('user_id', 'username', 'email_address', 'password', 'phone_number', 'first_name', 'last_name', 'created_at')


class CustomPreRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email_address', 'password', 'created_at', 'code')
    list_display_links = ('user_id', 'username', 'email_address')
    search_fields = ('user_id', 'username', 'email_address', 'password','created_at', 'code')
    list_filter = ('user_id', 'username', 'email_address', 'password', 'created_at', 'code')


admin.site.register(User, CustomUserAdmin)
admin.site.register(PreRegistration, CustomPreRegistrationAdmin)
