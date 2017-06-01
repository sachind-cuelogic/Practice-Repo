from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^practice/test/create/$', 'assessment.views.create_practice_test',
        name='practice_test_create'),
	url(r'^practice/test/take/$', 'assessment.views.take_practice_test',
        name='practice_test_take'),
	url(r'^practice/test/result/$', 'assessment.views.practice_test_result',
        name='practice_test_result'),
	url(r'^check/results/$', 'assessment.views.check_results',
        name='check_results'),
)
