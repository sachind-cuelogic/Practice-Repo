from django.conf import settings
from rest_framework import serializers
from comment_app.non_null_serializer import BaseSerializer
from django.db import models
from comment_app.models import (
    Comments,
    CommentAndVote
)



class CommentSerializer(BaseSerializer):
    """
    Serializer for comment
    """

    class Meta:
        model = Comments
        read_only_fields = ('id', 'created_at')


class CommentAndVoteSerializer(BaseSerializer):
    """
    Serializer for CommentAndVote
    """

    class Meta:
        model = CommentAndVote
        read_only_fields = ('id',)


class ListCommentAndVoteSerializer(BaseSerializer):
    """
    Serializer for CommentAndVote
    """
    class Meta:
        model = CommentAndVote
        fields = ('id', 'user')


class UserCommentListSerializer(BaseSerializer):
    user_liked = serializers.SerializerMethodField('get_user_comment_like')

    def get_user_comment_like(self, obj):
        
        if self.context and self.context.get('request'):
            if obj.user:
                user_id = self.context.get('request').user.id
                comment_object = CommentAndVote.objects.filter(user=user_id,
                                                               comment=obj.id)
                if len(comment_object):
                    return True
        return False

    class Meta:
        model = Comments
        fields = ('id', 'comment_text', 'attachment', 'user', 'user_liked', 'created_at')
        depth = 2
