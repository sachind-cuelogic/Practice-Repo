import base64
from django import template

from account.models import UserProfile
from knowledgebase.models import (
    QuestionAnswer,
    QuestionAnswerFlag,
    Category,
    Topic,
)

register = template.Library()


@register.assignment_tag
def get_question_hash(question_id):
    question_id = str(question_id)
    if question_id:
        question_id_hash = base64.b64encode(question_id)
        return question_id_hash
    else:
        raise TypeError("'None' Qusestion Id provided")


@register.assignment_tag
def can_publish(user_type=None):
    """
    This method used for template tag
    it takes user type,
    checks it and returns None if Normal user
    """
    if user_type == UserProfile.UserTypes.ADMINISTRATOR.value or user_type == UserProfile.UserTypes.MENTOR.value:
        return True
    return False


@register.filter(name='categoryobj')
def categoryobj(valuelist):
    if valuelist is not None:
        return [categoryobj for value in valuelist for categoryobj in Category.objects.filter(id=value)]


@register.filter(name='topicobj')
def topicobj(valuelist):
    if valuelist is not None:
        return [topicobj for value in valuelist for topicobj in Topic.objects.filter(id=value)]


@register.assignment_tag(name='get_url_hash')
def get_url_hash(**kwargs):
    """
    This method used for template tag
    it takes url parametrs and create its hash and returns it
    """

    url = \
        'category={0}&topic={1}&difficulty={2}&search_query={3}'.format(kwargs['active_category'
            ], kwargs['active_topic'], kwargs['active_difficulty'],
            kwargs['search_query'])
    return base64.urlsafe_b64encode(url)


@register.assignment_tag(name='get_hash')
def get_hash(name):
    """
    This method used for template tag
    it takes url parametrs and create its hash and returns it
    """
    return base64.urlsafe_b64encode(name)


@register.assignment_tag
def url_encode(q_id, next_param):
    if q_id is None:
        q_id = ""
    url = "question_id="+str(q_id)+"&next="+next_param
    if next_param == 'None':
        url = "question_id="+str(q_id)
    encoded_url = base64.urlsafe_b64encode(url)
    return encoded_url


@register.assignment_tag
def get_page_list(page_list, current_page):
    if current_page == 1:
        new_page_list = page_list[current_page-1:current_page+4]
    elif current_page == 2:
        new_page_list = page_list[current_page-2:current_page+3]
    else:
        new_page_list = page_list[current_page-3:current_page+2]
    return new_page_list


@register.assignment_tag
def check_user(review_note_user_id, loggedin_user_id):
    if review_note_user_id == loggedin_user_id:
        return True
    return False


@register.assignment_tag
def check_if_flagged(question_id):
    if question_id:
        question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
        question_flag = QuestionAnswerFlag.objects.filter(
            question=question_instance,
            is_delete=False)
        if len(question_flag) > 0:
            return True
        return False


@register.assignment_tag
def get_flag_errors(question_id):
    if question_id:
        question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
        question_flag = QuestionAnswerFlag.objects.filter(
            question=question_instance,
            is_delete=False)
        return question_flag


@register.assignment_tag
def can_delete(user_type=None, current_user=None, question_id=None):
    """
    This method used for template tag
    it takes user type,
    checks it and returns if that user can delete the question
    """
    try:
        question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
        if user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
            return True
        elif question_instance.user == current_user:
            return True
    except ValueError:
        return False


@register.assignment_tag
def check_flagged(question_id, current_user):
    try:
        question_instance = QuestionAnswer.objects.get(is_delete=False, id=question_id)
    except QuestionAnswer.DoesNotExist:
        question_instance = None
    try:
        if QuestionAnswerFlag.objects.get(user=current_user, question=question_instance, is_delete=False):
            return False
    except QuestionAnswerFlag.DoesNotExist:
        return True


@register.filter(name='get_mentor')
def get_mentor(valuelist):
    if valuelist is not None:
        for question_category in valuelist:
            for category in Category.objects.filter(name=question_category):
                return category.mentors.all()
