
from django.db import models
# from django.conf import settings
from register.models import User
from django.utils import timezone

# class UserProfileModel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(blank=True, null=True, max_length=100)
#     online_status = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return self.user.username
# Chat model
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else str(self.chat_id)
    
    class Meta:
        unique_together = ('chat_type', 'title')

# Participant model
class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} in chat {self.chat.title}"

# Message model
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.message_id} in chat {self.chat.title}"

# ChatAdmin model
class ChatAdmin(models.Model):
    chat_admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    appointed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} is admin of chat {self.chat.title}"

# MessageMedia model
class MessageMedia(models.Model):
    media_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Media {self.media_id} for message {self.message.message_id}"

# class ChatModel(models.Model):
#     sender = models.CharField(max_length=100, default=None)
#     message = models.TextField(null=True, blank=True)   
#     thread_name = models.CharField(null=True, blank=True, max_length=50)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.message
    
    
# class ChatNotification(models.Model):
#     chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_seen = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return self.user.username


# class ChatGroup(models.Model):
#     group_name = models.CharField(max_length=128, unique=True, blank=True)
#     admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
#     members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
#     is_private = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.group_name

# class GroupMessage(models.Model):
#     group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.CharField(max_length=300, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['-created']