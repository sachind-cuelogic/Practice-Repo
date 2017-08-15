from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from user_app import views

urlpatterns = [

    url(r'^register/$', views.CreateUserView.as_view(),
        name='create_user'),
    url(r'^login/$', views.LoginView.as_view(),
        name='login'),
    url(r'^update-pwd/$', views.UserUpdatePassword.as_view(),
        name='update_pwd'),
    url(r'^log-out/$', views.UserLogout.as_view(),
    	name='logout'),
    url(r'^confirm-signup/$', views.ConfirmSignup.as_view(),
    	name='ConfirmSignUP'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
