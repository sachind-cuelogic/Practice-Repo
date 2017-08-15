from private_message_app.non_null_serializer import BaseSerializer
from rest_framework import serializers
from private_message_app.models import (
    Message,
)


class MessageSerializer(BaseSerializer):
    """
    Serializer for update private message
    """
    class Meta:
        model = Message
        field = ('id', 'message_text', 'attachment', 'sender',
                 'receiver', 'ticket', 'from_user_read',
                 'to_user_read', 'from_user_delete', 'to_user_delete',)
        read_only_fields = ('id', 'from_user_read',)


class MessageViewSerializer(BaseSerializer):
    """
    Serializer for post private message
    """
    class Meta:
        model = Message
        field = ('id', 'message_text', 'attachment', 'sender',
                 'receiver', 'from_user_read',
                 'to_user_read', 'from_user_delete', 'to_user_delete',)
        read_only_fields = ('id', 'from_user_read',)
        exclude = ['ticket']
        depth = 2


class MessageExportSerializer(BaseSerializer):
    """
    Serializer for export private messages in pdf
    """
    class Meta:
        model = Message
        field = ('message_text', 'sender',
                 'ticket', 'created_at',)
