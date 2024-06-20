from django.db import models
from django.utils import timezone
from register.models import User

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model
    code = models.CharField(max_length=8)
    code_sent_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)