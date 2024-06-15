from django.db import models
from django.utils import timezone
from .utils import user_profile_picture_path

class User(models.Model):
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