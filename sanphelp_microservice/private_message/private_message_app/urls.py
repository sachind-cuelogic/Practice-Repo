from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from private_message_app import views

urlpatterns = [
    url(r'^private-message/$',
        views.MessageList.as_view(),
        name='private_message_view'),

    url(r'^private-message/update/(?P<id>[0-9]+)/$',
        views.MessageActivity.as_view(),
        name='private_message_activity_view'),

    # url(r'^private-message/export/(?P<id>[0-9]+)/$',
    #     views.MessageExportView.as_view(),
    #     name='private_message_export_view'),
     
]

urlpatterns = format_suffix_patterns(urlpatterns)
