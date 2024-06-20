from django.contrib import admin

from .models import *


class CustomPasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code', 'code_sent_at', 'created_at', 'user')
    list_display_links = ('user_id', 'code', 'user')
    search_fields = ('user_id', 'code', 'code_sent_at', 'created_at', 'user')
    list_filter = ('user_id', 'code', 'code_sent_at', 'created_at', 'user')


admin.site.register(PasswordReset, CustomPasswordResetAdmin)