from __future__ import absolute_import

from celery import task
from django.utils import timezone

from user_notifications_app.conf import (THRESHOLD_DAYS_FOR_SYSTEM_NOTIFICATION_REMOVAL,
                           THRESHOLD_DAYS_FOR_USER_NOTIFICATION_REMOVAL)
from mobile_notifications_app.models import UserNotifications


#############################################################################################
## Scheduled Task
#############################################################################################

@task()
def remove_system_generated_notifications():
    """
    Periodic Task
    This task will run everyday.
    This task will remove all system generated notifications
    This will be used for system tuning
    """
    kwargs_filter = {"notification_type": UserNotifications.NotificationType.SYSTEM_GENERATED.value}
    for noti in UserNotifications.objects.filter(**kwargs_filter):
        if (timezone.now() - noti.reported_date).days > THRESHOLD_DAYS_FOR_SYSTEM_NOTIFICATION_REMOVAL:
            noti.delete()


@task()
def remove_user_generated_notifications():
    """
    Periodic Task
    This task will run everyday.
    This task will remove all system generated notifications
    This will be used for system tuning
    """
    kwargs_filter = {"notification_type": UserNotifications.NotificationType.USER_OWNED.value}
    for noti in UserNotifications.objects.filter(**kwargs_filter):
        if (timezone.now() - noti.reported_date).days > THRESHOLD_DAYS_FOR_USER_NOTIFICATION_REMOVAL:
            noti.delete()

#############################################################################################
## Scheduled Task
#############################################################################################
