from push_notifications.models import APNSDevice, GCMDevice
from mobile_notifications_app.models import UserBadgeCount,UserNotifications
from mobile_notifications_app import helper


def getCurrentBadgeCount(user):
    user_badge_obj = UserBadgeCount.objects.filter(user=user)
    if user_badge_obj:
        return user_badge_obj[0].badge_count
    return 0


def send_notifications_to_device(list_user, message, params):
    android_device = GCMDevice.objects.filter(user__in=list_user)
    if android_device:
        send_notifications(android_device, message, params)

    ios_device = APNSDevice.objects.filter(user__in=list_user)
    if ios_device:
        send_notifications(ios_device, message, params)


def send_notifications(device, message, params):
    if len(device) < 2:
        user_badge_count = getCurrentBadgeCount(device[0].user)
        device.send_message(message, badge=user_badge_count, extra=params)
    else:
        device.send_message(message, extra=params)

def send_dummy_notification(users, message, params):
    notification_type = UserNotifications.NotificationType.USER_SCENARIOS.value
    helper.store_user_notifications(users,
                                    message, params, notification_type)
    send_notifications_to_device(
        users, message, params)
