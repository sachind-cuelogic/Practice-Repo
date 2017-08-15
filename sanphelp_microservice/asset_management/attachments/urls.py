from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from attachments import views

urlpatterns = [
    url(r'^assets/$',
        views.AssetsManagementCreateView.as_view(),
        name='user_assets_management'),
    url(r'^assets/multipart/$',
        views.AssetsManagementCreateViewMultipart.as_view(),
        name='user_multipart_assets_management'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
