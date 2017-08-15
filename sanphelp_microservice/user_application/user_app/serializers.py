from rest_framework import serializers

from user_app.non_null_serializer import BaseSerializer
from user_app.models import User


class UserSerializer(BaseSerializer):
    """
    Serializer for registering new users.
    This class excepts users details validates them
    and returns user object.
    """
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id', 'password', 'email',
            'full_name', 'phone_number', 'country_code', 'role',)
        read_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create(
                id = validated_data['id'],
                email = validated_data['email'],
                full_name = validated_data.get('full_name', ''),
                role = validated_data['role'],
                is_active = True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserMobileNoSerializer(BaseSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'country_code',)


class UserUpdateSerializer(BaseSerializer):
    """
    Serializer for registering new users.
    This class excepts users details validates them
    and returns user object.
    """
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id', 'password', 'email',
            'full_name', 'phone_number', 'country_code', 'role')
        read_only_fields = ('id', 'password', 'email', 'role',)
