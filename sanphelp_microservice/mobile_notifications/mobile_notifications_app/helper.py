import json

from mobile_notifications_app.models import (
    UserNotifications,
    UserBadgeCount
)


def store_user_notifications(users, message, param, notification_type):
    user_notifications = []
    for user in users:
        user_notifications.append(UserNotifications(
            user=user,
            notification_text=message,
            notification_param=json.dumps(param),
            notification_type=notification_type))
        user_badge, created = UserBadgeCount.objects.get_or_create(user=user)

        user_badge.badge_count += 1
        user_badge.save()

    UserNotifications.objects.bulk_create(user_notifications)
