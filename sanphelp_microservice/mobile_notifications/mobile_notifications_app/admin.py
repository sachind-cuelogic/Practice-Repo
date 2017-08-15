from django.contrib import admin
from mobile_notifications_app.models import UserNotifications,UserBadgeCount
# Register your models here.
admin.site.register(UserNotifications)
admin.site.register(UserBadgeCount)
