from django.conf.urls import patterns, url
from knowledgebase.views import *


BASE64_PATTERN = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'

urlpatterns = patterns('',
    url(r'^question/add/$', 'knowledgebase.views.question_answer_add',
        name='question_answer_add'),
    url(r'^question/add/success/$',
        'knowledgebase.views.question_answer_success',
        name='question_answer_success'),
    url(r'^question/list/$',
        'knowledgebase.views.question_list',
        name="question_list"),
    url(r'^question/list/publish$',
        'knowledgebase.views.question_publish_list',
        name="question_publish_list"),
    url(r'^question/list/submit$',
        'knowledgebase.views.question_submit_list',
        name="question_submit_list"),
    url(r'^question/list/draft$',
        'knowledgebase.views.question_draft_list',
        name="question_draft_list"),
    url(r'^notifications/view/all/(?P<user_id>\d+)/$', 'knowledgebase.views.viewe_all_notifications',
        name='viewe_all_notifications'),

    # following urls are used for ajax autocomplete purpose
    url(r'^api/categories/list/$', 'knowledgebase.views.categories_list',
        name='categories_list'),
    url(r'^api/topics/list/$', 'knowledgebase.views.topics_list',
        name='topics_list'),

    url(r'^api/notifications/get/$', 'knowledgebase.views.get_notifications',
        name='get_notifications'),
    url(r'^api/notifications/count/$', 'knowledgebase.views.get_notifications_count',
        name='get_notifications_count'),
    url(r'^api/notifications/viewed/$', 'knowledgebase.views.viewed_notifications',
        name='viewed_notifications'),
        url(r'^api/notifications/notified/$', 'knowledgebase.views.set_notifications_notified',
        name='set_notifications_notified'),

    url(r'^api/search/topics/$', 'knowledgebase.views.get_topics',
        name='topics_get'),

    # Following urls are used for view category,questions & answers,search in View knowledgebase
    url(r'^categories/view/$', 'knowledgebase.views.category_view',
        name='category_view'),
    url(r'^question/answer/view/$', 'knowledgebase.views.view_knowledgebase',
        name='view_knowledgebase'),
    url(r'^questions/search/$', 'knowledgebase.views.search_question',
        name='search_question'), 

    url(r'^question/review/$', 'knowledgebase.views.question_review',
        name='question_review'),
    url(r'^question/review/publish/$', 'knowledgebase.views.question_review_publish',
        name='question_review_publish'),
    url(r'question/publish', 'knowledgebase.views.question_publish_reject',
        name='question_publish'),
    url(r'question/review/submit/$', 'knowledgebase.views.question_review_submit',
        name='question_review_submit'),
    url(r'question/review/flag/$', 'knowledgebase.views.question_review_flag',
        name='question_review_flag'),

    # following urls are used for Question Review Notes
    url(r'^question/review/note$', 'knowledgebase.views.question_review_note',
        name='question_review_note'),
    url(r'question/reviews$', 'knowledgebase.views.question_get_reviews',
        name='question_get_reviews'),

    # Following url are used for view knowledgebase and search in View knowledgebase
    url(r'^questions/search/$', 'knowledgebase.views.search_question',
        name='search_question'),

    # Following url are used to flag question.
    url(r'^question/flag/$', 'knowledgebase.views.question_flag',
        name='question_flag'),
    url(r'^question/unflag/$', 'knowledgebase.views.question_unflag',
        name='question_unflag'),
    url(r'^question/flag/quantity/$', 'knowledgebase.views.flag_quantity_user',
        name='flag_quantity_user'),
    url(r'^question/delete/$', 'knowledgebase.views.question_delete',
        name='question_delete'),
)
