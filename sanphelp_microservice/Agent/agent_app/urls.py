from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from agent_app import views

urlpatterns = [

    url(r'^agent/register/$',
        views.CreateAgentUserView.as_view(), name='create_agent'),
    
    # url(r'^agent/update/(?P<id>[0-9]+)/$',
    #     views.UpdateAgentUserView.as_view(), name='update_agent'),
    # url(r'^agent/performance/rating/$',
    #     views.AgentPerformanceView.as_view(), name='agent_performance'),
    # url(r'^admin/login/$', views.AdminLoginView.as_view(),
    #     name='login'),
    # url(r'^admin/home/search/$',
    #     views.AdminHomeSearchView.as_view(),
    #     name='home_search'),
    # url(r'^update/agent/account/$',
    #     views.UpdateAgentAccountView.as_view(),
    #     name='update_agent_account'),

]

urlpatterns = format_suffix_patterns(urlpatterns)