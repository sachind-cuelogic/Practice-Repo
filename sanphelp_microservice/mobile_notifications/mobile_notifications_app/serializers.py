from push_notifications.models import APNSDevice, GCMDevice

from mobile_notifications_app.non_null_serializer import BaseSerializer
from mobile_notifications_app.models import (UserNotifications,
                                         UserBadgeCount)


class RegisterIOSDeviceSerializer(BaseSerializer):
    class Meta:
        model = APNSDevice
        fields = ("id", "active",
                  "registration_id", "user",)
        read_only_fields = ("id",)


class RegisterAndroidDeviceSerializer(BaseSerializer):
    class Meta:
        model = GCMDevice
        fields = ("id", "active",
                  "registration_id", "user",)
        read_only_fields = ("id",)


class UserNotificationsSerializer(BaseSerializer):
    class Meta:
        model = UserNotifications
        read_only_fields = ("id")


class UserReadNotificationsSerializer(BaseSerializer):
    class Meta:
        model = UserNotifications
        read_only_fields = ("id", "user",
                            "notification_text", "notification_param",
                            "notification_type")


class UserBadgeCountSerializer(BaseSerializer):
    class Meta:
        model = UserBadgeCount
        read_only_fields = ("id")
