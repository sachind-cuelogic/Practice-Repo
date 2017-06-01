import json
import re
import base64

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404, redirect,render_to_response
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from core.utils import get_latest_entries
from core.utils import pagination
from knowledgebase.forms import QuestionAnswerAddForm
from account.models import UserProfile
from core.utils import(
    metor_category_verification,
    view_access_verification,
    unflag_access_verification,
)
from taggit.models import Tag
from knowledgebase.models import (
    Category,
    QuestionAnswer,
    Notification,
    QuestionReviewNote,
    QuestionAnswerFlag,
    Topic,
)
from knowledgebase.knowledgebase_utilities import(
    category_add,
    count_user_notifications,
    generate_comment_notification,
    get_notifications_ids,
    get_user_notifications,
    prcess_notifications,
    topic_add,
)


# This function redirects to home page on error.
def validateurl(func):
    def if_exist_url(request):
        namespace = request.resolver_match.namespace
        valid_url = reverse('{0}:{1}'.format(namespace, func.func_name))
        if request.path == valid_url:
            try:
                return func(request)
            except Exception:
                return redirect('core_index')
    return if_exist_url


def getStringFromList(lst):
    return ",".join(lst)


def getListFromString(str):
    return [x.strip() for x in str.split(',') if x != ""]


@view_access_verification
@require_http_methods(["GET", "POST"])
def question_answer_add(request):
    redirect_to = None
    question_answer_id = None
    param = request.REQUEST.get('param', '')
    list_param = base64.urlsafe_b64decode(param.encode("utf-8")).split('&')
    notification_message = None
    question_answer = None
    try:
        redirect_to = list_param[1].split('=')[1]
        question_answer_id = list_param[0].split('=')[1]
    except IndexError:
        pass

    try:
        if request.REQUEST['page']:
            redirect_to = request.REQUEST.get(
                'next', '') + '&page=' + request.REQUEST.get('page', '')
    except KeyError:
        pass
    if question_answer_id is not None:
        try:
            question_answer = get_object_or_404(
                QuestionAnswer,
                is_delete=False,
                id=question_answer_id
            )
        except ValueError:
            question_answer = None

    if request.method == 'POST':
        redirect_to = request.POST.get('next')
        question_answer_add_form = QuestionAnswerAddForm(
            request.POST,
            instance=question_answer
        )
        if question_answer_add_form.is_valid():
            if request.POST['submit'] == 'save':
                if question_answer:
                    if question_answer.state != QuestionAnswer.QuestionAnswerState.DRAFT:
                        if request.user != question_answer.user:
                            Notification.add_new_notification(
                                4,
                                request.user,
                                question_answer,
                                question_answer.user
                            )
                state = QuestionAnswer.QuestionAnswerState.DRAFT
            elif request.POST['submit'] == 'publish':
                state = QuestionAnswer.QuestionAnswerState.PUBLISH
            elif request.POST['submit'] == 'submission':
                state = QuestionAnswer.QuestionAnswerState.SUBMIT
            else:
                HttpResponseBadRequest("ERROR: Bad request input!!!")

            user_id = request.user.id
            categories_name = question_answer_add_form.cleaned_data['categories']
            category_id = category_add(categories_name, request.user)

            topics_name = question_answer_add_form.cleaned_data['topics']
            topic_id = topic_add(topics_name, request.user, category_id)

            question_answer_add = question_answer_add_form.save(commit=False)
            question_answer_add.current_user = request.user
            question_answer_add.state = state


            if question_answer is None:
                question_answer_add.user_id = user_id
                question_answer = question_answer_add
            question_answer_add.save()

            tags = getListFromString(request.POST["tags"])
            for tag in tags:
                question_answer_add.tags.add(tag)

            question_answer_add.categories = ([category_id.id])
            question_answer_add.topics = ([topic_id.id])
            if request.POST['submit'] == 'save':
                question_answer = question_answer_add
                messages.success(request, "Your question has been Drafted...!")
            else:
                if request.POST['submit'] == 'publish':
                    redirect_to = reverse('ppi-knowledgebase:question_publish_list')
                    messages.success(request, "Your question has been Published...!")
                elif request.POST['submit'] == 'submission':
                    messages.success(request, "Your question has been Submitted for review...!")
                    redirect_to = reverse('ppi-knowledgebase:question_submit_list')
                return HttpResponseRedirect(redirect_to)
        else:
            messages.error(request, "Error occurred. Please try again!")

    else:
        question_answer_add_form = QuestionAnswerAddForm(
            instance=question_answer,
            user=request.user
        )
        if question_answer_add_form.initial:
            question_answer_add_form.initial['categories'] = ''.join([
                cat.name for cat in question_answer.categories.all()])
            question_answer_add_form.initial['topics'] = ''.join([
                cat.name for cat in question_answer.topics.all()])
            question_answer_add_form.initial['tags'] = question_answer.getAllTags()
    return render(
        request,
        'knowledgebase/add_question.html',
        {
            'add_question_form': question_answer_add_form,
            'qa': question_answer,
            'complete_message': notification_message,
            'next': redirect_to
        }
    )


def question_answer_success(request):
    return render(request, 'knowledgebase/add_question_success.html')


@require_http_methods(["GET", "POST"])
def categories_list(request):
    if request.is_ajax():
        user_input = request.GET.get('term', '')
        categories = Category.objects.filter(name__icontains=user_input)[:20]
        results = []
        for category in categories:
            results.append({
                'id': category.id,
                'label': category.name,
                'value': category.name,
            })

        data = json.dumps(results)
    else:
        data = 'Not valid request'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@require_http_methods(["GET", "POST"])
def topics_list(request):
    if request.is_ajax():
        user_input = request.GET.get('term', '')
        topics = Topic.objects.filter(name__icontains=user_input)[:20]
        results = []
        for topic in topics:
            results.append({
                'id': topic.id,
                'label': topic.name,
                'value': topic.name,
            })

        data = json.dumps(results)
    else:
        data = 'Not valid request'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# This function is for ALL tab in Question Reviews
@metor_category_verification
@require_http_methods(["GET", "POST"])
def question_review(request):
    search_query = ""
    question_all = QuestionAnswer.objects.filter(is_delete=False,
        categories__in=Category.objects.filter(mentors__in=[request.user.id]),
        state=QuestionAnswer.QuestionAnswerState.PUBLISH)

    if request.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
        question_all = QuestionAnswer.objects.filter(state=QuestionAnswer.QuestionAnswerState.PUBLISH,
            is_delete=False)

    if request.POST.get('query'):
        search_query = request.POST.get('query')
        request.GET = request.GET.copy()
        request.GET['page'] = 1
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        question_all = question_all.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))
    question_paginated = pagination(request, question_all)
    question_array = [question_paginated]
    active_tab = "all"
    return render(request, 'knowledgebase/question_review_list.html',
                  {'question_array': question_array, 'active_tab': active_tab,'search':search_query})


# This function is called for PUBLISH tab in Question Reviews
@metor_category_verification
@require_http_methods(["GET", "POST"])
def question_review_publish(request):
    search_query = ""
    if request.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
        question_publish = QuestionAnswer.objects.filter(
            state=QuestionAnswer.QuestionAnswerState.PUBLISH,
            is_delete=False)
    else:
        question_publish = QuestionAnswer.objects.filter(
            categories__mentors=request.user,
            is_delete=False,
            state=QuestionAnswer.QuestionAnswerState.PUBLISH)

    if request.POST.get('query'):
        search_query = request.POST.get('query')
        request.GET = request.GET.copy()
        request.GET['page'] = 1
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        question_publish = question_publish.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))

    question_paginated = pagination(request, question_publish)
    question_array = [question_paginated]
    active_tab = "publish"
    return render(request, 'knowledgebase/question_review_list.html',
                  {'question_array': question_array, 'active_tab': active_tab,'search':search_query})


# This function is called for Flag Tab in Question Review
@metor_category_verification
@require_http_methods(["GET", "POST"])
def question_review_flag(request):
    question_id = []
    question_list = []
    search_query = ""

    question = QuestionAnswerFlag.objects.filter(is_delete=False)
    

    for questionanswer_id in question:
        question_id.append(questionanswer_id.question.id)
    question_id = set(question_id)
    question_id = list(question_id)
    try:
        if request.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
            for flag_question_id in question_id:
                question_list.append(QuestionAnswer.objects.get(is_delete=False,
                                                                id=flag_question_id))
        else:
            for flag_question_id in question_id:
                question_list.append(QuestionAnswer.objects.get(is_delete=False,
                                                                categories__mentors=request.user,
                                                                id=flag_question_id))
    except QuestionAnswer.DoesNotExist:
        question_list = []
    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        for flag_question_id in question_list:
            question_list = QuestionAnswer.objects.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)),id=flag_question_id.id)

    question_paginated = pagination(request, question_list)
    question_array = [question_paginated]
    active_tab = "flag"
    return render(request, 'knowledgebase/question_review_list.html',
                  {'question_array': question_array, 'active_tab': active_tab,'search':search_query})


# This function is called for REVIEW tab in Question Reviews
@metor_category_verification
@require_http_methods(["GET", "POST"])
def question_review_submit(request):
    search_query = ""
    if request.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
        question_review = QuestionAnswer.objects.filter(
            is_delete=False,
            state=QuestionAnswer.QuestionAnswerState.SUBMIT)
    else:
        question_review = QuestionAnswer.objects.filter(
            is_delete=False,
            categories__mentors=request.user,
            state=QuestionAnswer.QuestionAnswerState.SUBMIT)

    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        question_review = question_review.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))


    question_paginated = pagination(request, question_review)
    question_array = [question_paginated]
    active_tab = "review"
    return render(request, 'knowledgebase/question_review_list.html',
                  {'question_array': question_array, 'active_tab': active_tab,'search':search_query})


# this function adds Review and displays it.
@require_http_methods(["GET", "POST"])
def question_review_note(request):
    if request.method == "GET":
        if request.GET['question_id']:
            question_notice = request.GET.get('note')
            question_id = request.GET.get('question_id')
            question = QuestionAnswer.objects.get(is_delete=False, id=question_id)
            question_review_note = QuestionReviewNote.objects.create(
                question_note_id=question,
                note=question_notice,
                user=request.user)
            question_review_note.save()

            result = []
            if question.user.userprofile.first_name:
                user_name = question_review_note.user.userprofile.first_name
            else:
                user_name = question_review_note.user
            result.append({
                'review_note_id': question_review_note.id,
                'user': str(user_name),
                'email': str(question_review_note.user),
                'date': str(question_review_note.date_time.date()),
                'note_time_hour': str(question_review_note.date_time.hour),
                'note_time_min': str(question_review_note.date_time.minute),
                'review_note': question_review_note.note,
                'review_author': question_review_note.user.id,
                'loggedin_user': request.user.id,
            })
            generate_comment_notification(request.user, question, 2)
            review_notes = render_to_string('knowledgebase/question_review_note.html',
                                            {'results': result})
            return HttpResponse(review_notes)
    return HttpResponse("Failed")


# This function gets all review notes when question is loaded.
@require_http_methods(["GET", "POST"])
def question_get_reviews(request):
    if request.method == "GET":
        if request.GET['question_id']:
            question_id = request.GET.get('question_id')
            question_user_reviews = QuestionReviewNote.objects.filter(
                question_note_id=question_id).order_by('date_time')
            result = []

            for review in question_user_reviews:
                if review.user.userprofile.first_name:
                    user_name = review.user.userprofile.first_name
                else:
                    user_name = review.user
                result.append({
                    'review_note_id': review.id,
                    'user': str(user_name),
                    'email': str(review.user),
                    'date': str(review.date_time.date()),
                    'note_time_hour': str(review.date_time.hour),
                    'note_time_min': str(review.date_time.minute),
                    'review_note': review.note,
                    'review_author': review.user.id,
                    'loggedin_user': request.user.id,
                })

            review_notes = render_to_string('knowledgebase/question_review_note.html',
                                            {'results': result})
            return HttpResponse(review_notes)
    return HttpResponse("Failed")


@require_http_methods(["GET", "POST"])
def question_publish_reject(request):
    if request.method == "POST":
        question_id = request.POST.get('question_id')
        question_state = request.POST.get('question_state')

        if question_id and question_state:
            question_answer = QuestionAnswer.objects.get(is_delete=False,
                                                         id=question_id)

            if question_state == "Publish":
                question_answer.state = QuestionAnswer.QuestionAnswerState.PUBLISH
                message = _("Question Published")

            if question_state == "Reject":
                question_answer.state = QuestionAnswer.QuestionAnswerState.DRAFT
                message = _("Question Rejected")
                Notification.add_new_notification(
                    3,
                    request.user,
                    question_answer,
                    question_answer.user
                )
            question_answer.current_user = request.user
            question_answer.save()
            return HttpResponse(message)
    return HttpResponse("Failed!!")


# This view displays all Users question in all tab
def question_list(request):
    """
    this function gets hashed email, decodes it and use it for profile viewing
    """
    search_query = ""
    questionsanswer_paginated = None
    questionsanswer_list = QuestionAnswer.objects.filter(
        is_delete=False,
        user=request.user
    ).order_by('-date_added')

    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        questionsanswer_list = questionsanswer_list.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))
    question_paginated = pagination(request, questionsanswer_list)
    questionsanswer_paginated = question_paginated
    active_tab = "all"
    return render(
        request,
        'knowledgebase/question_list.html',
        {'questionsanswer_list': questionsanswer_paginated,
         'active_tab': active_tab,'search':search_query}
    )


def question_draft_list(request):
    """
    this function gets hashed email, decodes it and use it for profile viewing
    """
    search_query= ""
    questionsanswer_paginated = None
    questionsanswer_list = QuestionAnswer.objects.filter(
        user=request.user,
        is_delete=False,
        state=QuestionAnswer.QuestionAnswerState.DRAFT
    ).order_by('-date_added')

    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        questionsanswer_list = questionsanswer_list.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))
    if questionsanswer_list:
        question_paginated = pagination(request, questionsanswer_list)
        questionsanswer_paginated = question_paginated

    active_tab = "draft"
    return render(
        request,
        'knowledgebase/question_list.html',
        {'questionsanswer_list': questionsanswer_paginated,
         'active_tab': active_tab,'search':search_query}
    )


def question_publish_list(request):
    """
    this function gets hashed email, decodes it and use it for profile viewing
    """
    search_query = ""
    questionsanswer_paginated = None
    questionsanswer_list = QuestionAnswer.objects.filter(
        user=request.user,
        is_delete=False,
        state=QuestionAnswer.QuestionAnswerState.PUBLISH
    ).order_by('-date_added')

    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))
    if search_query is not None:
        questionsanswer_list = questionsanswer_list.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))

    question_paginated = pagination(request, questionsanswer_list)
    questionsanswer_paginated = question_paginated
    active_tab = "publish"
    return render(
        request,
        'knowledgebase/question_list.html',
        {'questionsanswer_list': questionsanswer_paginated,
         'active_tab': active_tab,'search':search_query}
    )


def question_submit_list(request):
    """
    this function gets hashed email, decodes it and use it for profile viewing
    """
    search_query = ""
    questionsanswer_paginated = None
    questionsanswer_list = QuestionAnswer.objects.filter(
        user=request.user,
        is_delete=False,
        state=QuestionAnswer.QuestionAnswerState.SUBMIT
    ).order_by('-date_added')

    if request.POST.get('query'):
        search_query = request.POST.get('query')
    elif request.GET.get('query'):
        search_query = base64.urlsafe_b64decode(request.GET.get('query').encode("utf-8"))

    if search_query is not None:
        questionsanswer_list = questionsanswer_list.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)))

    question_paginated = pagination(request, questionsanswer_list)
    questionsanswer_paginated = question_paginated

    active_tab = "submit"
    return render(
        request,
        'knowledgebase/question_list.html',
        {'questionsanswer_list': questionsanswer_paginated,
         'active_tab': active_tab,'search':search_query}
    )


# This function gets all the topic of selected category in dropdown.
def get_topics(request):
    results = {}
    mimetype = 'application/json'
    if request.is_ajax():
        category_id = request.POST.getlist('category_id[]')
        if len(category_id) > 0:
            topics = [topic for category in category_id for topic in
                      Topic.objects.filter(categories=category)]
            results['topics'] = topics
        else:
            topics = [topic for topic in Topic.objects.all()]
            results['topics'] = topics
        html = render_to_string('knowledgebase/filtersubtemplate.html',
                                {'topic_menu': topics})
        return HttpResponse(html)
    else:
        data = 'Not valid request'
        return HttpResponse(data, mimetype)

def get_topicrelated_questions(list_questions,get_topics,difficulty_list=[],get_categories=[]):
    if len(difficulty_list) != 0:
        if get_categories:
            [list_questions.append(question) for category in get_categories 
                                             for topic in get_topics
                                             for difficulty in difficulty_list
                                             for question in QuestionAnswer.objects.filter(categories=category,topics=topic,difficulty_level=difficulty,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             if not question in list_questions]
        else:
            [list_questions.append(question) for topic in get_topics
                                             for difficulty in difficulty_list
                                             for question in QuestionAnswer.objects.filter(topics=topic,difficulty_level=difficulty,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             if not question in list_questions]
    else:
        if get_categories:
            [list_questions.append(question) for category in get_categories 
                                             for topic in get_topics
                                             for question in QuestionAnswer.objects.filter(categories=category,topics=topic,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             if not question in list_questions]
        else:
            [list_questions.append(question) for topic in get_topics
                                             for question in QuestionAnswer.objects.filter(topics=topic,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             if not question in list_questions]
    return list_questions

def search_filter(list_questions,get_search_query,get_category_list=[],get_topic_list=[],get_difficulty_list=[]):
    categories = [category for category_id in get_category_list
                           for category in Category.objects.filter(id=category_id)]
    topics = [topic for topic_id in get_topic_list
                    for topic in Topic.objects.filter(id=topic_id)]
    if len(get_category_list) != 0:
        get_categories = [category for category_id in get_category_list
                                   for category in Category.objects.filter(id=category_id,name__iexact=get_search_query)]
        if len(get_topic_list) != 0:
            get_topics = [topic for topic_id in get_topic_list
                                for topic in Topic.objects.filter(id=topic_id,name__iexact=get_search_query)]
            if get_topics:
                if len(get_difficulty_list) != 0:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_difficulty_list,get_categories=get_categories)
                else:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_categories=get_categories)
        else:
            get_topics = [topic for category in get_category_list
                                for topic in Topic.objects.filter(categories=category,name__iexact=str(get_search_query))]
            if get_categories:
                [get_topics.append(topic) for category in get_categories
                                          for topic in Topic.objects.filter(categories=category)
                                          if not topic in get_topics]
            if get_topics:
                if len(get_difficulty_list)!=0:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_difficulty_list,get_categories=get_categories)
                else:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_categories=get_categories)
    else:
        if len(get_topic_list) != 0:
            get_categories = [category for category in Category.objects.filter(name__iexact=str(get_search_query))]
            get_topics = [topic for topic_id in get_topic_list
                                for topic in Topic.objects.filter(id=topic_id,name__iexact=str(get_search_query))]
            if get_categories:
                    [get_topics.append(topic) for category in get_categories
                                              for topic_id in get_topic_list
                                              for topic in Topic.objects.filter(id=topic_id,categories=category)
                                              if not topic in get_topics]
            if get_topics:
                if len(get_difficulty_list)!=0:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_difficulty_list,get_categories=get_categories)
                else:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_categories=get_categories)
        else:
            get_categories = [category for category in Category.objects.filter(name__iexact=str(get_search_query))]
            get_topics = [topic for topic in Topic.objects.filter(name__iexact=str(get_search_query))]
            if len(get_difficulty_list)!=0:
                if get_categories:
                    [list_questions.append(question) for category in get_categories
                                                     for difficulty in get_difficulty_list
                                                     for question in QuestionAnswer.objects.filter(categories=category,difficulty_level=difficulty,
                                                         is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                                     if not question in list_questions]
                if get_topics:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_difficulty_list)
            else:
                if get_categories:
                    [list_questions.append(question) for category in get_categories
                                                     for question in QuestionAnswer.objects.filter(categories=category,is_delete=False,
                                                         state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                                     if not question in list_questions]
                if get_topics:
                    list_questions = get_topicrelated_questions(list_questions,get_topics,get_difficulty_list)
                [list_questions.append(question) for question in QuestionAnswer.objects.filter(is_delete=False,
                                                     state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                                 for tags in question.tags.all()
                                                 if str(tags) == str(get_search_query)
                                                 if not question in list_questions]
    return list_questions

# This function gets all the questions related to search query.
@validateurl
def search_question(request):
    if request.GET.get('param'):
        data = base64.urlsafe_b64decode(request.GET.get('param').encode("utf-8"))
        get_list = data.split('&')
        search_query = replacestring(get_list[3].split('=')[1])[0]
    else:
        if request.GET.get('search'):
            search_query = base64.urlsafe_b64decode(request.GET.get('search').encode("utf-8"))
    category_menu = Category.objects.all()
    topic_menu = Topic.objects.all()
    if search_query:
        get_questions = [questionlist for questionlist in
                         QuestionAnswer.objects.filter(Q(question__icontains=str(search_query))
                         | Q(answer__icontains=str(search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
        get_questions = search_filter(get_questions,search_query)
        question_paginated = pagination(request, get_questions)
        if get_questions:
            dictionary = {
                'list_questions': question_paginated,
                'topic_menu': topic_menu,
                'category_menu': category_menu,
                'search': search_query,
            }
        else:
            message = 'Sorry no results found related to search'
            dictionary = {
                'message': message,
                'topic_menu': topic_menu,
                'category_menu': category_menu,
                'search': search_query,
            }
    else:
        get_questions = QuestionAnswer.objects.all()
        question_paginated = pagination(request, get_questions)
        dictionary = {
            'list_questions': 'question_paginated',
            'topic_menu': topic_menu,
            'category_menu': category_menu,
            'search': search_query,
        }
    return render(request, 'knowledgebase/view_knowledgebase.html',
                  dictionary)


def get_filters():
    """
    This function gets all the category,topics and
    questions(only published questions).
    """
    category_menu = Category.objects.all()
    topic_menu = Topic.objects.all()
    list_questions = QuestionAnswer.objects.filter(state=QuestionAnswer.QuestionAnswerState.PUBLISH,is_delete=False)
    return (category_menu, topic_menu, list_questions)


# This function filters unicode string.
def replacestring(data):
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace(" ", "")
    data = data.replace("u'", "")
    data = data.replace("'", "")
    data = re.sub(r'\s', '', data).split(',')
    data = [x for x in data if x]
    return data


# This function filters according to user selection and calls appropriate function.
def get_filter_results(request, templatename, function_flag):
    if request.GET:
        data = request.GET
        if request.GET.get('param') is not None:
            data = base64.urlsafe_b64decode(request.GET.get('param').encode("utf-8"))
            get_list = data.split('&')
            get_category_list = replacestring(get_list[0].split('=')[1])
            get_topic_list = replacestring(get_list[1].split('=')[1])
            get_difficulty_list = \
                replacestring(get_list[2].split('=')[1])
            get_search_query = replacestring(get_list[3].split('=')[1])
            if len(get_search_query) > 0:
                get_search_query = replacestring(get_list[3].split('=')[1])[0]
            else:
                get_search_query = ""
        else:
            get_category_list = \
                replacestring(data.getlist('category')[0])
            get_topic_list = replacestring(data.getlist('topic')[0])
            get_difficulty_list = \
                replacestring(data.getlist('difficulty')[0])
            get_search_query = data.get('search_query_input')
    else:
        data = request.POST
        get_category_list = data.getlist('category_filter')
        get_topic_list = data.getlist('topic_filter')
        get_difficulty_list = data.getlist('difficulty_filter')
        get_search_query = data.get('search_query_input')
    dictionary = {}
    if get_search_query is None:
        get_search_query = ''

    if len(get_category_list) != 0:
        dictionary = category_filter(request, get_category_list,
                                     get_topic_list,
                                     get_difficulty_list,
                                     get_search_query)
    elif len(get_topic_list) != 0 and len(get_category_list) == 0:
        dictionary = topic_filter(request, get_category_list,
                                  get_topic_list, get_difficulty_list,
                                  get_search_query)
    else:
        dictionary = difficulty_filter(request, get_category_list,
                                       get_topic_list,
                                       get_difficulty_list,
                                       get_search_query)
    if function_flag == 1:
        if 'list_questions' in dictionary:
            resultset = get_latest_entries(dictionary['category_menu'], dictionary['list_questions'])
            dictionary['list_questions'] = resultset
        if 'topics' in dictionary:
            resultset = get_latest_entries(dictionary['category_menu'], dictionary['topics'])
            dictionary['topics'] = resultset
    return render(request, templatename, dictionary)


# This funtion is used get list of pagination objects depending on current url,
# i.e for category view categories are paginates and for knowledgebase view questions are paginated.
def get_pagination_list(request, question_category, list_questions):
    if request.path == reverse('ppi-knowledgebase:category_view'):
        categories_paginated = pagination(request, question_category)
        question_paginated = list_questions
        return categories_paginated, question_paginated
    else:
        categories_paginated = question_category
        question_paginated = pagination(request, list_questions)
        return categories_paginated, question_paginated


@validateurl
def category_view(request):
    templatename = 'knowledgebase/view_category.html'
    function_flag = 1
    return get_filter_results(request, templatename, function_flag)


def get_questionrelated_search(request):
        (category_menu, topic_menu, list_questions) = get_filters()
        question = base64.urlsafe_b64decode(request.GET.get('qparam').encode("utf-8"))
        get_questions = QuestionAnswer.objects.filter(question=question,
                                                      state=QuestionAnswer.QuestionAnswerState.PUBLISH,
                                                      is_delete=False)

        for question in get_questions:
            question_category = question.categories.all()[0]

        question_category = [category.id for category in
                             Category.objects.filter(name=question_category)]
        topic_menu = [topic for topic in
                      Topic.objects.filter(categories=question_category[0])]
        question_paginated = pagination(request, get_questions)
        results = {'list_questions': question_paginated,
                       'topic_menu': topic_menu,
                       'category_menu': category_menu,
                       'searchflag': 1,
                       'activecategory': question_category}
        return results

def get_categoryrelated_search(request):
    (category_menu, topic_menu, list_questions) = get_filters()
    category_name = base64.urlsafe_b64decode(request.GET.get('cparam').encode("utf-8"))
    category = Category.objects.filter(name=category_name)
    category_id = [category.id for category in
                   Category.objects.filter(name=category_name)]
    topic_menu = [topic for topic in
                  Topic.objects.filter(categories=category)]
    get_questions = \
        QuestionAnswer.objects.filter(is_delete=False,
                                      categories=category,
                                      state=QuestionAnswer.QuestionAnswerState.PUBLISH)

    question_paginated = pagination(request, get_questions)
    if get_questions:
        resultset = {'list_questions': question_paginated,
                     'topic_menu': topic_menu,
                     'category_menu': category_menu,
                     'searchflag': 1,
                     'activecategory': category_id}
    else:
        message = 'Sorry no results found...Try again or Clear filter'
        resultset = {'message': message,
                     'topic_menu': topic_menu,
                     'category_menu': category_menu,
                     'searchflag': 1,
                     'activecategory': category_id}
    return resultset


def get_topicrelated_search(request):
    (category_menu, topic_menu, list_questions) = get_filters()
    topic_name = base64.urlsafe_b64decode(request.GET.get('tparam').encode("utf-8"))
    topic_id = Topic.objects.get(name = topic_name)
    category_name = topic_id.categories.all()
    category_list = list(set(category_name))
    display_topic = [topic.id for topic in Topic.objects.filter(id=topic_id.id)]
    category_id = [category.id for categ in category_list 
                               for category in Category.objects.filter(name=categ.name)]
    get_questions = \
        QuestionAnswer.objects.filter(is_delete=False,
                                      topics = topic_id.id,
                                      state=QuestionAnswer.QuestionAnswerState.PUBLISH)

    question_paginated = pagination(request, get_questions)
    if get_questions:
        resultset = {'list_questions': question_paginated,
                     'topic_menu': topic_menu,
                     'category_menu': category_menu,
                     'searchflag': 1,
                     'activecategory': category_id,
                     'activetopic':display_topic}
    else:
        message = 'Sorry no results found...Try again or Clear filter'
        resultset = {'message': message,
                     'topic_menu': topic_menu,
                     'category_menu': category_menu,
                     'searchflag': 1,
                     'activecategory': category_id,
                     'activetopic':display_topic}
    return resultset


@validateurl
def view_knowledgebase(request):
    if request.GET.get('qparam'):
        resultset = get_questionrelated_search (request)
        return render(request, 'knowledgebase/view_knowledgebase.html',
                      resultset)

    if request.GET.get('cparam'):
        resultset = get_categoryrelated_search (request)
        return render(request, 'knowledgebase/view_knowledgebase.html',
                      resultset)

    if request.GET.get('tparam'):
        resultset = get_topicrelated_search (request)
        return render(request, 'knowledgebase/view_knowledgebase.html',
                      resultset)
    templatename = 'knowledgebase/view_knowledgebase.html'
    function_flag = 0
    return get_filter_results(request, templatename, function_flag)

# This function returns categories and topics of question list.
def category_topic(list_questions):
    categories = []
    topics = []
    for question in list_questions:
        question_category = question.categories.all()[0]
        for category in Category.objects.filter(name=question_category):
            categories.append(category)

        question_topic = question.topics.all()[0]
        for topic in Topic.objects.filter(name=question_topic):
            topics.append(topic)

    categories = list(set(categories))
    topics = list(set(topics))

    return (categories, topics)


# This filters out category selection scenario.
def category_filter(
    request,
    get_category_list,
    get_topic_list,
    get_difficulty_list,
    get_search_query,
):
    if len(get_topic_list) != 0:
        return category_topic_difficulty(request, get_category_list,
                                         get_topic_list,
                                         get_difficulty_list,
                                         get_search_query)
    else:
        return category_difficulty(request, get_category_list,
                                   get_difficulty_list,
                                   get_search_query)


# This filters out category,topic,difficulty,search query(for knowlegdebase view) related scenarios.
def category_topic_difficulty(
    request,
    get_category_list,
    get_topic_list,
    get_difficulty_list,
    get_search_query,
):
    (category_menu, topic_menu, list_questions) = get_filters()
    categories = [category for category_id in get_category_list
                  for category in
                  Category.objects.filter(id=category_id)]
    topic_menu = [topic for category in categories for topic in
                  Topic.objects.filter(categories=category)]
    topics = [topic for topic_id in get_topic_list for topic in
              Topic.objects.filter(id=topic_id)]

    if len(get_difficulty_list) != 0:
        if get_search_query:
            list_questions = [question for category in
                              get_category_list for topic in
                              get_topic_list for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(
                                  difficulty_level=difficulty,
                                  categories=category, is_delete=False,
                                  topics=topic).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
            list_questions = search_filter(list_questions,get_search_query,get_category_list=get_category_list,get_topic_list=get_topic_list,get_difficulty_list=get_difficulty_list)
            [list_questions.append(question) for category in categories
                                             for topic in topics
                                             for difficulty in get_difficulty_list
                                             for question in QuestionAnswer.objects.filter(categories=category,topics=topic,is_delete=False,
                                                 difficulty_level=difficulty,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for category in
                              get_category_list for topic in
                              get_topic_list for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(difficulty_level=difficulty, is_delete=False,
                              categories=category, topics=topic,state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    else:
        if get_search_query:
            list_questions = [question for category in categories
                              for topic in topics for question in
                              QuestionAnswer.objects.filter(topics=topic, is_delete=False,
                              categories=category).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
            list_questions = search_filter(list_questions,get_search_query,get_category_list=get_category_list,get_topic_list=get_topic_list)
            [list_questions.append(question) for category in categories
                                             for topic in topics
                                             for question in QuestionAnswer.objects.filter(categories=category,topics=topic,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for topic in topics
                              for category in categories
                              for question in
                              QuestionAnswer.objects.filter(topics=topic,
                              categories=category,is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    if list_questions:
        (question_category, question_topic) = \
            category_topic(list_questions)
        (categories_paginated, question_paginated) = \
            get_pagination_list(request, question_category,
                                list(set(list_questions)))
        return {
            'categories': categories_paginated,
            'category_menu': category_menu,
            'topics': question_topic,
            'topic_menu': topic_menu,
            'list_questions': question_paginated,
            'activedifficulty': get_difficulty_list,
            'activecategory': get_category_list,
            'activetopic': get_topic_list,
            'search': get_search_query}
    message = 'Sorry no results found...Try again or Clear filter'
    return {
        'message': message,
        'topics': topics,
        'topic_menu': topic_menu,
        'category_menu': category_menu,
        'activecategory': get_category_list,
        'activetopic': get_topic_list,
        'activedifficulty': get_difficulty_list,
        'search': get_search_query}


# This filters out category,difficulty,search query(for knowlegdebase view)
# related scenario.
def category_difficulty(
    request,
    get_category_list,
    get_difficulty_list,
    get_search_query,
):
    (category_menu, topic_menu, list_questions) = get_filters()

    categories = [category for category_id in get_category_list
                  for category in
                  Category.objects.filter(id=category_id)]
    topic_menu = [topic for category in categories for topic in
                  Topic.objects.filter(categories=category)]
    if len(get_difficulty_list) != 0:
        if get_search_query:
            list_questions = [question for category in
                              get_category_list for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(difficulty_level=difficulty, is_delete=False,
                              categories=category).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
            list_questions = search_filter(list_questions,get_search_query,get_category_list=get_category_list,get_difficulty_list=get_difficulty_list)
            [list_questions.append(question) for category in categories
                                             for difficulty in get_difficulty_list
                                             for question in QuestionAnswer.objects.filter(categories=category,is_delete=False,
                                                 difficulty_level=difficulty,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for category in
                              get_category_list for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(difficulty_level=difficulty, is_delete=False,
                              categories=category,state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    else:
        if get_search_query:
            list_questions = [question for category in
                              get_category_list for question in
                              QuestionAnswer.objects.filter(categories=category, is_delete=False).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
            list_questions = search_filter(list_questions,get_search_query,get_category_list=get_category_list)
            [list_questions.append(question) for category in categories
                                             for question in QuestionAnswer.objects.filter(categories=category,
                                                 is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for category in categories
                              for question in
                              QuestionAnswer.objects.filter(categories=category, is_delete=False,
                                                            state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    if list_questions:
        (question_category, question_topic) = \
            category_topic(list_questions)
        list_questions = list(set(list_questions))
        (categories_paginated, question_paginated) = \
            get_pagination_list(request, question_category,
                                list_questions)
        return {
            'topics': question_topic,
            'topic_menu': topic_menu,
            'category_menu': category_menu,
            'categories': categories,
            'activecategory': get_category_list,
            'list_questions': question_paginated,
            'activedifficulty': get_difficulty_list,
            'search': get_search_query}
    message = 'Sorry no results found...Try again or Clear filter'
    return {
        'message': message,
        'category_menu': category_menu,
        'activecategory': get_category_list,
        'topic_menu': topic_menu,
        'activedifficulty': get_difficulty_list,
        'search': get_search_query}

# This filters out topic,difficulty,search query(for knowlegdebase view) related scenario.
def topic_filter(
    request,
    get_category_list,
    get_topic_list,
    get_difficulty_list,
    get_search_query,
):
    (category_menu, topic_menu, list_questions) = get_filters()

    categories = [category for topic in get_topic_list for category in
                  Category.objects.filter(topic__id=topic)]
    topics = [topic for topic_id in get_topic_list for topic in
              Topic.objects.filter(id=topic_id)]
    categories = list(set(categories))
    categories_paginated = pagination(request, categories)
    if len(get_difficulty_list) != 0:
        if get_search_query:
            list_questions = [question for topic in get_topic_list
                              for difficulty in get_difficulty_list
                              for question in
                              QuestionAnswer.objects.filter(is_delete=False, difficulty_level=difficulty,
                              topics=topic,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                              .filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)))]
            list_questions = search_filter(list_questions,get_search_query,get_topic_list=get_topic_list,get_difficulty_list=get_difficulty_list)
            [list_questions.append(question) for topic in topics
                                             for difficulty in get_difficulty_list
                                             for question in QuestionAnswer.objects.filter(topics=topic,is_delete=False,
                                                 difficulty_level=difficulty,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for topic in get_topic_list
                              for difficulty in get_difficulty_list
                              for question in
                              QuestionAnswer.objects.filter(is_delete=False, difficulty_level=difficulty,
                              topics=topic,state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    else:
        if get_search_query:
            list_questions = [question for topic in get_topic_list
                              for question in
                              QuestionAnswer.objects.filter(is_delete=False, topics=topic,state=QuestionAnswer.QuestionAnswerState.PUBLISH).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)))]
            list_questions = search_filter(list_questions,get_search_query,get_topic_list=get_topic_list)
            [list_questions.append(question) for topic in topics
                                             for question in QuestionAnswer.objects.filter(topics=topic,is_delete=False,
                                                 state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for topic in get_topic_list
                              for question in
                              QuestionAnswer.objects.filter(is_delete=False,
                                                            topics=topic,
                                                            state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
    if list_questions:
        (question_category, question_topic) = \
            category_topic(list_questions)
        (categories_paginated, question_paginated) = \
            get_pagination_list(request, question_category,
                                list_questions)
        return {
            'categories': categories_paginated,
            'category_menu': category_menu,
            'topics': question_topic,
            'topic_menu': topics,
            'activetopic': get_topic_list,
            'list_questions': question_paginated,
            'activedifficulty': get_difficulty_list,
            'search': get_search_query}
    message = 'Sorry no results found...Try again or Clear filter'
    return {
        'message': message,
        'topics': topics,
        'topic_menu': topic_menu,
        'activetopic': get_topic_list,
        'category_menu': category_menu,
        'activedifficulty': get_difficulty_list,
        'search': get_search_query}

# This filters out basic(none selected),difficulty,search query(for knowlegdebase view) related scenario.
def difficulty_filter(
    request,
    get_category_list,
    get_topic_list,
    get_difficulty_list,
    get_search_query,
):
    (category_menu, topic_menu, list_questions) = get_filters()
    categories_paginated = pagination(request, category_menu)
    if len(get_difficulty_list) != 0:
        if get_search_query:
            list_questions = [question for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(is_delete=False,difficulty_level=difficulty).filter(Q(question__icontains=str(get_search_query))
                              | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
            list_questions = search_filter(list_questions,get_search_query,get_difficulty_list=get_difficulty_list)
            [list_questions.append(question) for difficulty in get_difficulty_list
                                             for question in QuestionAnswer.objects.filter(difficulty_level=difficulty,
                                                is_delete=False,state=QuestionAnswer.QuestionAnswerState.PUBLISH)
                                             for tags in question.tags.all() if str(tags) == str(get_search_query)
                                             if not question in list_questions]
        else:
            list_questions = [question for difficulty in
                              get_difficulty_list for question in
                              QuestionAnswer.objects.filter(is_delete=False,
                                                            difficulty_level=difficulty,
                                                            state=QuestionAnswer.QuestionAnswerState.PUBLISH)]
        if list_questions:
            (question_category, question_topic) = \
                category_topic(list_questions)
            (categories_paginated, question_paginated) = \
                get_pagination_list(request, question_category,
                                    list_questions)
            return {
                'topics': question_topic,
                'topic_menu': topic_menu,
                'category_menu': category_menu,
                'categories': categories_paginated,
                'list_questions': question_paginated,
                'activedifficulty': get_difficulty_list,
                'search': get_search_query}
        message = 'Sorry no results found...Try again or Clear filter'
        return {
            'message': message,
            'category_menu': category_menu,
            'activecategory': get_category_list,
            'topic_menu': topic_menu,
            'activetopic': get_topic_list,
            'activedifficulty': get_difficulty_list,
            'search': get_search_query}
    (categories_paginated, question_paginated) = \
        get_pagination_list(request, category_menu, list_questions)
    if get_search_query:
        get_questions = [questionlist for questionlist in
                         QuestionAnswer.objects.filter(Q(question__icontains=str(get_search_query))
                        | Q(answer__icontains=str(get_search_query)),state=QuestionAnswer.QuestionAnswerState.PUBLISH,is_delete=False)]
        get_questions = search_filter(get_questions,get_search_query)
        question_paginated = pagination(request, get_questions)
        if get_questions:
            return {
                'categories': categories_paginated,
                'category_menu': category_menu,
                'topics': topic_menu,
                'topic_menu': topic_menu,
                'list_questions': question_paginated,
                'activedifficulty': get_difficulty_list,
                'activecategory': get_category_list,
                'activetopic': get_topic_list,
                'search': get_search_query}
        else:
            message = \
                'Sorry no results found...Try again or Clear filter'
            return {
                'message': message,
                'category_menu': categories_paginated,
                'activecategory': get_category_list,
                'topic_menu': topic_menu,
                'activetopic': get_topic_list,
                'activedifficulty': get_difficulty_list,
                'search': get_search_query}
    else:
        return {
            'categories': categories_paginated,
            'category_menu': category_menu,
            'topics': topic_menu,
            'topic_menu': topic_menu,
            'list_questions': question_paginated,
            'activedifficulty': get_difficulty_list,
            'activecategory': get_category_list,
            'activetopic': get_topic_list,
            'search': get_search_query,}
    return {
        'categories': category_menu,
        'category_menu': category_menu,
        'topics': topic_menu,
        'topic_menu': topic_menu,
        'list_questions': list_questions,
        'activedifficulty': get_difficulty_list,
        'activecategory': get_category_list,
        'activetopic': get_topic_list,}


def get_notifications(request):
    if request.is_ajax():
        notifications = get_user_notifications(request.user)
        result = prcess_notifications(notifications[:5])
        data = json.dumps(result)
    else:
        data = 'Not valid request'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_notifications_count(request):
    if request.is_ajax():
        notifications = count_user_notifications(request.user)
        notification_ids = get_notifications_ids(notifications)
        notify = {}
        notify['count'] = str(len(notifications))
        notification_ids.append(notify)
        result = notification_ids
        data = json.dumps(result)
    else:
        data = '0'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def viewed_notifications(request):
    question_id = request.GET.get('question_id', None)
    notification_id = request.GET.get('notification_id', None)

    if question_id is not None and notification_id is not None:
        notification = Notification.objects.get(id=notification_id)
        notification.viewed = True
        notification.notified = True
        notification.save()
        url = 'question_id=' + str(notification.question.id) + '&next=/knowledgebase/question/list/?page=1'
        encoded_url = base64.urlsafe_b64encode(url)
        return HttpResponseRedirect(
            reverse(
                'ppi-knowledgebase:question_answer_add',
            ) + '?param=' + encoded_url
        )
    return HttpResponseRedirect('')


def viewe_all_notifications(request, user_id):
    notifications = get_user_notifications(request.user)
    for notification in notifications:
        notification.notified = True
        notification.save()
    notification_list = prcess_notifications(notifications)
    return render(
        request,
        'knowledgebase/view_notifications.html',
        {'notification_list': notification_list}
    )


def set_notifications_notified(request):
    if request.is_ajax():
        notification_id_list = request.POST.get('notification_id_list', None)
        notification_ids = json.loads(notification_id_list)
        id_list = [ids['notification_id'] for ids in notification_ids[:-1]]
        for notification in Notification.objects.filter(id__in=id_list):
            notification.notified = True
            notification.save()
        result = ''
        data = json.dumps(result)
    else:
        data = '0'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def question_flag(request):
    if request.method == "GET":
        if request.GET['question_id']:
            question_id = request.GET.get('question_id')
            question_id = question_id.split("-")[1]
            flag_message = request.GET.get('flag_message')
            flag_text = request.GET.get('flag_text')
            user = request.user
            response = []

            question_istance = QuestionAnswer.objects.get(is_delete=False,
                                                          id=question_id)
            try:
                if flag_message:
                    flag_text += ". (" + flag_message + ")"

                QuestionAnswerFlag.objects.get(user=user,
                                               question=question_istance,
                                               is_delete=False)
                response.append({
                    'id': question_id,
                    'message': "You have already flagged this question"
                })
                return HttpResponse(json.dumps(response), 'application/json')

            except QuestionAnswerFlag.DoesNotExist or MultipleObjectsReturned:
                QuestionAnswerFlag.objects.create(
                    user=user,
                    question=question_istance,
                    text=flag_text)

                question_review_note = QuestionReviewNote.objects.create(
                    question_note_id=question_istance,
                    note="FLAG BECAUSE:-" + flag_text,
                    user=request.user)
                question_review_note.save()

                response.append({
                    'id': question_id,
                    'message': "Question has been flagged"
                })
                return HttpResponse(json.dumps(response), 'application/json')

    return HttpResponse("Failed")


@login_required
@unflag_access_verification
def question_unflag(request):
    if request.method == "GET":
        if request.GET['question_id']:
            question_id = request.GET.get('question_id')
            result = []
            question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
            flags = QuestionAnswerFlag.objects.filter(question=question_instance,
                                                      is_delete=False)

            for flag in flags:
                flag.is_delete = True
                flag.save()
            message = _("Flags has been removed from this question.")

            result.append({
                'message': message
            })
            return HttpResponse(json.dumps(result), 'application/json')
    return HttpResponse("Failed")


@login_required
def flag_quantity_user(request):
    user = request.user
    flags = QuestionAnswerFlag.objects.filter(user=user,
                                              date=timezone.now().date(),
                                              is_delete=False)
    total_flag = len(flags)
    return HttpResponse(total_flag)


@login_required
def question_delete(request):
    if request.GET['question_id']:
        question_id = request.GET.get('question_id')
        question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
        question_answer_add_form = QuestionAnswerAddForm(instance=question_instance)
        qa_instance = question_answer_add_form.save(commit=False)
        qa_instance.current_user = request.user
        qa_instance.is_delete = True
        qa_instance.save()
        messages.info(request, "Your question has been Deleted...!")
        return HttpResponse("Question Deleted")
    return HttpResponse("Failed")
