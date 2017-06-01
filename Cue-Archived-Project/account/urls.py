from django.conf.urls import patterns, url

from account import views

BASE64_PATTERN = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'

urlpatterns = patterns(
    '',
    url(r'^profile/edit/',
        views.profile_edit,
        name="profile_edit"),
    url(r'^profile/view/(?P<uidb64>{})'.format(BASE64_PATTERN),
        views.profile_view,
        name="profile_view"),
)
