from django.utils import timezone
from django.db import models
import django.contrib.auth.hashers as hasher
import os
from django.contrib.auth.models import User

from django.forms import ValidationError


# Extended User model with public key.
class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.BinaryField(null= True)



class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expires_at__gte=timezone.now())


def validate_message_content(value):
    if len(value) > 1000:
        raise ValidationError('Message is too long')
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.CharField(max_length=1000, validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=30))
    is_encrypted = models.BooleanField(default=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

