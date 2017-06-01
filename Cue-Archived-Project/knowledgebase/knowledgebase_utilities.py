import re

from django.core.urlresolvers import reverse
from itertools import chain

from account.models import UserProfile
from knowledgebase.models import(
    Category,
    Topic,
    Notification,
    QuestionAnswer,
)
from ppiauth.models import PPIUser

# Further we need to pass link with messages by using 2D array
NOTIFICATON_LIST = [
    'new question has been submitted for review in %s category',
    'new question has been published in %s category',
    '%s commented on %s ',
    '%s rejected %s question',
    '%s drafted %s question',
    '%s flagged %s question',
    '%s flag on %s question has been marked as mis-leading',
    '%s flag on %s question has been marked as unflaged',
    '%s deleted %s question'
]


def find_mentors(questionanswer, sender):
    resultes = []
    categories = questionanswer.categories.all()
    for category in categories:
        mentors = category.mentors.all().exclude(id=sender.id)
        resultes.append(mentors)
    return set(resultes)


def category_add(category_name, user_obj):
    """
    This method will return category object if available
    or it will create new category and return its object
    """
    try:
        category = Category.objects.get(name__iexact=category_name)
    except Category.DoesNotExist:
        category = Category(name=category_name, user=user_obj)
        category.save()
    return category


def topic_add(topic_name, user_obj, category_id):
    """
    This method will return topic if available with associated category
    or it will check the availability of topic
    if it is available it will add category to its categories field
    or it will create new topic with selected category and return it
    """
    try:
        topic = Topic.objects.get(name__iexact=topic_name, categories=category_id)
    except Topic.DoesNotExist:
        try:
            topic = Topic.objects.get(name=topic_name)
            topic.categories.add(category_id)
        except Topic.DoesNotExist:
            topic = Topic(name=topic_name, user=user_obj)
            topic.save()
            topic.categories.add(category_id)
        topic.save()
    return topic


def get_user_notifications(user):
    notification = []
    notification = Notification.objects.filter(
        recipient=user
    ).order_by('-timestamp')
    return notification


def count_user_notifications(user):
    notification = []
    notification = Notification.objects.filter(
        notified=False,
        recipient=user
    )
    return notification


def prcess_notifications(notifications):
    result = []
    for notification in notifications:
        notify = {}
        temp = NOTIFICATON_LIST[notification.notification_message_index]
        notify['question_id'] = notification.question.id
        notify['notification_id'] = notification.id
        if notification.notification_message_index < 2:
            notify['notification_txt'] = temp % (
                notification.question.categories.all(
                ).values('name')[0]['name']
            )
        else:
            question_string = notification.question.question
            cleanr =re.compile('<.*?>')
            cleaned_question_string = re.sub(cleanr,'', question_string)
            if len(question_string) > 47:
                question_string = question_string[:47] + '...'
            question_string = "'" + question_string + "'"
            notify['notification_txt'] = temp % (
                str(notification.sender.userprofile.first_name),
                cleaned_question_string
            )
        try:
            if QuestionAnswer.objects.get(id=notification.question.id,
                                          is_delete=False):
                notification_link = reverse(
                    'ppi-knowledgebase:viewed_notifications') + '?question_id=' + str(notification.question.id)
        except QuestionAnswer.DoesNotExist:
            notification_link = "#"
        notify['link'] = str(notification_link)
        notify['viewed'] = notification.viewed
        notify['timestamp'] = str(notification.timestamp.date())
        result.append(notify)
    return result


def get_notifications_ids(notifications):
    result = []
    for notification in notifications:
        notify = {}
        notify['notification_id'] = notification.id
        result.append(notify)
    return result


def generate_comment_notification(sender, questionanswer, notification_type):
    mentor_list = list(find_mentors(questionanswer, sender))[0]
    administrator_list = [user for user in PPIUser.objects.filter(
    ).exclude(
        id=sender.id
            ) if user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value]
    administrator_list.append(questionanswer.user)
    user_list_set = set(chain(mentor_list, administrator_list))
    for user in user_list_set:
        if sender.id != user.id:
            Notification.add_new_notification(
                notification_type=notification_type,
                sender=sender,
                questionanswer=questionanswer,
                recipient=user
            )
