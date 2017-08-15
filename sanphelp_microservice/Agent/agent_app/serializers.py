from rest_framework import serializers

# from accounts.models import Category
from agent_app.models import Agent
from agent_app.non_null_serializer import BaseSerializer


class AgentSerializer(BaseSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True,
                                                  allow_null=True,
                                                  read_only=True
                                                  )

    class Meta:
        model = Agent

        fields = ('id', 'is_admin', 'is_supervisor', 'account', 'user',
                  'assendents', 'is_active', 'category',
                  'created_by', 'created_at', 'total_resolved_issues',
                  'total_open_issue', 'gender', 'profile_picture')

        read_only_fields = ('id', 'created_at', 'total_resolved_issues',
                            'total_open_issue',)


class AgentUpdateSerializer(BaseSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True,
                                                  allow_null=True,
                                                  read_only=True
                                                  )

    class Meta:
        model = Agent
        read_only_fields = ('id', 'created_at', 'total_resolved_issues',
                            'total_open_issue', 'account', 'user',
                            'created_by',)
