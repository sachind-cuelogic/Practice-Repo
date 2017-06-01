from django.conf.urls import patterns, url

from ppiauth.views import *


urlpatterns = patterns(
    '',
    url(r'^registration/$', 'ppiauth.views.registration',
        name='registration'),
    url(r'^registration/success/$', 'ppiauth.views.registration_success',
        name='registration_success'),
    url(r'^registration/confirm/(?P<activation_key>\w+)/$',
        'ppiauth.views.registration_confirm', name='registration_confirm'),

    url(r'^registration/resend/activation/key/$',
        'ppiauth.views.resend_activation_key', name='resend_activation_key'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout'),
    # NOTE: login is handled in the middleware class PPIAuthLoginMiddleware

    url(r'^password/change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/auth/password/change/done/',
         'template_name': 'ppiauth/password_change_form.html'},
        name='password_change'),
    url(r'^password/change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'ppiauth/password_change_done.html'},
        name='password_change_done'),

    url(r'^password/recovery/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/auth/password/recovery/done/',
         'current_app': 'ppiauth',
         'email_template_name': 'ppiauth/password_reset_email.html',
         'template_name': 'ppiauth/password_reset_form.html',
         'subject_template_name': 'ppiauth/password_reset_subject.txt'},
        name='password_recovery'),
    url(r'^password/recovery/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'current_app': 'ppiauth',
         'template_name': 'ppiauth/password_reset_done.html'},
        name='password_recovery_done'),

    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'ppiauth/password_reset_confirm.html',
         'post_reset_redirect': '/auth/password/reset/done',
         'current_app': 'ppiauth'},
        name='password_reset_confirm'),
    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'current_app': 'ppiauth',
         'template_name': 'ppiauth/password_reset_complete.html'},
        name='password_reset_done'),

    # Note:- This url is used to check if the account is not active when
    # you click forget password
    url(r'^verify/email/$', 'ppiauth.views.email_verify',
        name='email_verify'),
)
