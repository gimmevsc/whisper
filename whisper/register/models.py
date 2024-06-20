from django.db import models
from django.utils import timezone
from .utils import user_profile_picture_path
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email_address, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email Address field must be set')
        
        email_address = self.normalize_email(email_address)
        user = self.model(username=username, email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email_address, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Required fields for Django authentication
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email_address'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

class PreRegistration(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email_address = models.EmailField()
    password = models.CharField(max_length=128)
    code = models.CharField(max_length=8)
    code_sent_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
# class ChatGroup(models.Model):
#     group_name = models.CharField(max_length=128, unique=True, blank=True)
#     groupchat_name = models.CharField(max_length=128, null=True, blank=True)
#     admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
#     users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
#     members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
#     is_private = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.group_name
    
# class GroupMessage(models.Model):
#     group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.CharField(max_length=300, blank=True, null=True)
#     # file = models.FileField(upload_to='files/', blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['-created']