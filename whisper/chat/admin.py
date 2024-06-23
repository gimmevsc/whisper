from django.contrib import admin
from chat.models import Chat, Participant, Message, MessageMedia, ChatModel


class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'chat_type', 'title', 'created_at', 'updated_at')
    list_display_links = ('chat_id', 'title')
    list_filter = ('chat_type', 'created_at', 'updated_at')
    search_fields = ('chat_id', 'title')

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'user', 'chat', 'joined_at', 'is_admin')
    list_filter = ('joined_at', 'is_admin')
    list_display_links = ('participant_id', 'user')
    search_fields = ('user__username', 'chat__title')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'chat', 'sender', 'message_content', 'sent_at', 'is_read', 'is_deleted')
    list_filter = ('chat', 'sender', 'sent_at', 'is_read', 'is_deleted')
    list_display_links = ('message_id', 'message_content')
    search_fields = ('message_id', 'message_content')

# class ChatAdminsAdmin(admin.ModelAdmin):
#     list_display = ('chat_admin_id', 'user', 'chat', 'appointed_at')
#     list_filter = ('appointed_at',)
#     list_display_links = ('chat_admin_id', 'user')
#     search_fields = ('user__username', 'chat__title')

class MessageMediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'message', 'media_type', 'file_path', 'uploaded_at')
    list_filter = ('media_type', 'uploaded_at')
    list_display_links = ('media_id', 'file_path')
    search_fields = ('message__message_id', 'file_path')

class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'thread_name', 'timestamp')
    list_filter = ('sender', 'thread_name', 'timestamp')
    list_display_links = ('sender',)
    search_fields = ('sender', 'message', 'thread_name')

admin.site.register(Chat, ChatAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)
# admin.site.register(ChatAdmin, ChatAdminsAdmin)
admin.site.register(MessageMedia, MessageMediaAdmin)
admin.site.register(ChatModel, ChatModelAdmin)
