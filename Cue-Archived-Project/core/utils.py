import datetime
import hashlib
import random

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from account.models import UserProfile
from knowledgebase.models import QuestionAnswer


def generate_activation_key(email):
    """
    It accepts email, encrypts it and returns back.
    """
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + email).hexdigest()
    return activation_key


def generate_expiry_timestamp():
    """
    It generates an expiry key of 2 days from the present day.
    """
    key_expires = timezone.now() + datetime.timedelta(2)
    return key_expires


def pagination(request,queryset,count=3):
    paginator = Paginator(queryset,count)
    page = request.GET.get('page')
    try:
        queryset_pagination = paginator.page(page)
    except PageNotAnInteger:
        queryset_pagination = paginator.page(1)
    except EmptyPage:
        queryset_pagination = paginator.page(paginator.num_pages)
    
    return queryset_pagination

def metor_category_verification(function):
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.user_type == UserProfile.UserTypes.NORMAL_USER.value:
            return HttpResponseRedirect(reverse('page_not_found'))
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def view_access_verification(function):
    def wrap(request, *args, **kwargs):
        flag = False
        if request.user.userprofile.user_type != UserProfile.UserTypes.ADMINISTRATOR.value:
            try:
                question_id = request.GET.get('question_id', None)
                try:
                    question = QuestionAnswer.objects.get(id=question_id)
                    if request.user.userprofile.user_type == UserProfile.UserTypes.NORMAL_USER.value:
                        if question.user != request.user:
                            flag = True
                    # elif request.user.userprofile.user_type == UserProfile.UserTypes.MENTOR.value:
                    else:
                        is_mentor = [i for i in question.categories.all() if request.user in i.mentors.all()]
                        if len(is_mentor) <= 0:
                            flag = True
                except ValueError:
                    pass
            except QuestionAnswer.DoesNotExist:
                pass

        if flag == False:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('page_not_found'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def unflag_access_verification(function):
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.user_type == UserProfile.UserTypes.NORMAL_USER.value:
            return HttpResponseRedirect(reverse('page_not_found'))
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


#This function will filter latest 5 objects of given queryset.
def get_latest_entries(categories,queryset):
    list_latest, cat_latest_entries = [], []
    for category in categories:
        for each in queryset:
            for cat in set(each.categories.all()):
                if cat == category:
                    if each:
                        list_latest.append(each)
                else:
                    continue
        if len(list_latest) > 0:
            list_latest = list_latest[:5]
            cat_latest_entries.append({category:list_latest})
        list_latest = []
    queryset = cat_latest_entries
    return queryset
