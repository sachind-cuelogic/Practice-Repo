from django.db import models
from enum import Enum

# Create your models here.
class UserBadgeCount(models.Model):
    user = models.CharField(max_length=100)
    badge_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_badge_count'


class UserNotifications(models.Model):

    class NotificationType(Enum):
        SYSTEM_GENERATED = 'System_Generated'
        USER_OWNED = 'User_Owned'
        USER_OFFERS = 'user_offers'
        USER_SCENARIOS = 'user_scenarios'
        COMPONENT_FAILURE = 'component_failure'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    user = models.CharField(max_length=100)
    notification_text = models.TextField(null=True, blank=True)
    notification_param = models.CharField(max_length=1000, null=True, blank=True)
    reported_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(null=True, max_length=50,
                                         choices=NotificationType.as_tuple())

    class Meta:
        db_table = 'user_notification'
