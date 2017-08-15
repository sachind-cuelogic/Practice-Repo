from django.db import models
from django.core.validators import RegexValidator

from django.utils import timezone
from enum import Enum

class Message(models.Model):
    """
    Base class for storing Messages.
    This messages are from chats between users
    and agent.
    """
    message_text = models.TextField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    sender = models.CharField(max_length=10, null=True, blank=True)
    receiver = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.CharField(max_length=10, null=True, blank=True)
    from_user_read = models.BooleanField(default=True)
    to_user_read = models.BooleanField(default=False)
    from_user_delete = models.BooleanField(default=False)
    to_user_delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.message_text

    class Meta:
        db_table = 'message'
