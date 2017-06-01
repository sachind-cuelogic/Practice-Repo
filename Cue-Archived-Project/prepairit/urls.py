from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import django.views.defaults

urlpatterns = patterns('',
    # Enable the URLs when implemented
    url(r'^$', 'core.views.index', name='core_index'),
    url(r'^page-not-found/$', 'core.views.page_not_found', name='page_not_found'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('ppiauth.urls', namespace='ppi-auth')),
    url(r'^account/', include('account.urls', namespace='ppi-accounts')),
    url(r'^knowledgebase/', include('knowledgebase.urls', namespace='ppi-knowledgebase')),
    url(r'^assessment/', include('assessment.urls',namespace='ppi-assessment')),
)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
