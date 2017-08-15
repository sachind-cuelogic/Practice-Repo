from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from mobile_notifications_app import views

urlpatterns = [
    url(r'^ios-device/register/$', views.RegisterIOSDevice.as_view(),
        name='create_ios_device'),
    url(r'^ios-device/modify/$', views.ModifyIOSDevice.as_view(),
        name='update_ios_device'),
    url(r'^ios-device/delete/$', views.RemoveIOSDevice.as_view(),
        name='delete_ios_device'),

    url(r'^android-device/register/$', views.RegisterAndroidDevice.as_view(),
        name='create_android_device'),
    url(r'^android-device/modify/$', views.ModifyAndroidDevice.as_view(),
        name='update_android_device'),
    url(r'^android-device/delete/$', views.RemoveAndroidDevice.as_view(),
        name='delete_android_device'),

    url(r'^device/notification/$', views.GetUserNotifications.as_view(),
        name='user_notification'),
    url(r'^device/notification/read/$', views.MarkUserNotificationsRead.as_view(),
        name='user_notification'),

    url(r'^user/badge-count/$', views.GetUserBadgeCount.as_view(),
        name='user-badge-count'),
    url(r'^user/reset-badge/$', views.ResetUserBadgeCount.as_view(),
        name='delete_android_device'),
    url(r'^dummy/notification/$', views.SendDummyNotification.as_view(),
        name='dummy_notification'),
    url(r'^component/notification/$', views.SendComponentNotification.as_view(),
        name='component_notification'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
