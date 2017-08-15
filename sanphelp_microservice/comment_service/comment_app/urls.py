from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from comment_app import views


urlpatterns = [

        	
	url(r'^comment/$',
        views.CommentCreateView.as_view(),
        name='comment'),

	url(r'^comment/(?P<id>[0-9]+)/$',
        views.CommentDetailView.as_view(),
        name='comment_update_list'),

	url(r'^comment/like/$',
        views.CommentVoteView.as_view(),
        name='comment_like'),

        # url(r'^comments/export/(?P<id>[0-9]+)/$',
        # views.CommentExportView.as_view(),
        # name='comments_export_view'),

]
