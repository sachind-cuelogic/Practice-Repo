from itertools import chain

from django_enumfield import enum
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete

from ppiauth.models import PPIUser
from account.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)

    user = models.ForeignKey(PPIUser, related_name="Author")
    mentors = models.ManyToManyField(PPIUser,
                                     blank=True,
                                     null=True,
                                     related_name="Mentor")
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def clean(self):
        if Category.objects.filter(name__iexact=self.name).exists():
            if not Category.objects.filter(name=self.name).exists():
                raise ValidationError("Category with this Name already exists")


@receiver(post_save, sender=Category)
def create_mentor_for_category(sender, instance=None,
                               created=False, **kwargs):
    """
    When a new user is created this fuctions creates a userprofile
    for that particular user.
    """
    if instance.mentors:
        for mentor in instance.mentors.all():
            if mentor.userprofile.user_type == UserProfile.UserTypes.NORMAL_USER.value:
                mentor.userprofile.user_type = UserProfile.UserTypes.MENTOR.value
                mentor.userprofile.save()


class Topic(models.Model):
    name = models.CharField(max_length=128,unique=True)
    user = models.ForeignKey(PPIUser)

    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = 'Topics'

    def __unicode__(self):
        return self.name

    def clean(self):
        if Topic.objects.filter(name__iexact=self.name).exists():
            if not Topic.objects.filter(name=self.name).exists():
                raise ValidationError("Topic with this Name already exists")


class QuestionAnswer(models.Model):

    # This class will declare the values for enum field
    # for Question and Answer state
    class QuestionAnswerState(enum.Enum):
        DRAFT = 1
        SUBMIT = 2
        PUBLISH = 3

    # This class will declare the values for enum
    # field for QuestionAnswer difficulty level
    class DifficultyLevels(enum.Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCE = 3

    question = models.TextField()
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    state = enum.EnumField(QuestionAnswerState)
    difficulty_level = enum.EnumField(DifficultyLevels)

    user = models.ForeignKey(PPIUser)
    categories = models.ManyToManyField(Category)
    topics = models.ManyToManyField(Topic)
    tags = TaggableManager(blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Questions and Answers'

    def __unicode__(self):
        return self.question
    
    def getAllTags(self):
        tags =  self.tags.all()
        str_list = []
        for tag in tags:
            str_list.append(tag.name)
        return ','.join(str_list)

# Generates notifications whenever a question answer is published or submited
@receiver(post_save, sender=QuestionAnswer)
def generate_notification(sender, instance, **kwargs):
    if instance.is_delete:
        Notification.notification_create(instance.current_user, instance, 8)
    elif instance.state == QuestionAnswer.QuestionAnswerState.PUBLISH:
        Notification.notification_create(instance.current_user, instance, 1)
    elif instance.state == QuestionAnswer.QuestionAnswerState.SUBMIT:
        Notification.notification_create(instance.current_user, instance, 0)


class Notification(models.Model):
    notification_message_index = models.IntegerField()
    viewed = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    recipient = models.ForeignKey(PPIUser, related_name="recipient")
    sender = models.ForeignKey(PPIUser, related_name="sender")
    question = models.ForeignKey(QuestionAnswer)
    timestamp = models.DateTimeField(auto_now_add=True)

    # notification is getting added.
    @classmethod
    def add_new_notification(cls, notification_type, sender, questionanswer, recipient):
        notification = Notification(
            notification_message_index=notification_type,
            sender=sender,
            question=questionanswer,
            recipient=recipient
        )
        notification.save()

    # Generates notification
    @classmethod
    def notification_create(cls, sender, questionanswer, notification_type):
        user_list = []
        if notification_type == 1:
            user_list = PPIUser.objects.all().exclude(id=sender.id)
            for user in user_list:
                cls.add_new_notification(
                    notification_type=notification_type,
                    sender=sender,
                    questionanswer=questionanswer,
                    recipient=user
                )

        elif notification_type != 1:
            mentor_list = []
            resultes = []
            categories = questionanswer.categories.all()
            for category in categories:
                mentors = category.mentors.all().exclude(id=sender.id)
                resultes.append(mentors)
            try:
                mentor_list = list(resultes)[0]
            except IndexError:
                pass

            administrator_list = [user for user in PPIUser.objects.filter(
            ).exclude(
                id=sender.id
            ) if user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value]
            user_list_set = chain(mentor_list, administrator_list)
            for user in user_list_set:
                cls.add_new_notification(
                    notification_type=notification_type,
                    sender=sender,
                    questionanswer=questionanswer,
                    recipient=user
                )


class QuestionReviewNote(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
    question_note_id = models.ForeignKey(QuestionAnswer)
    user = models.ForeignKey(PPIUser)

    def __unicode__(self):
        return self.note


class QuestionAnswerFlag(models.Model):
    user = models.ForeignKey(PPIUser)
    question = models.ForeignKey(QuestionAnswer)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

    @classmethod
    def flag_notification(cls, notification_type, instance):
        mentor_list = []
        resultes = []
        categories = instance.question.categories.all()
        for category in categories:
            mentors = category.mentors.all().exclude(id=instance.user.id)
            resultes.append(mentors)
        try:
            mentor_list = list(resultes)[0]
        except IndexError:
            pass
        administrator_list = [user for user in PPIUser.objects.filter(
        ).exclude(
            id=instance.user.id
        ) if user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value]
        user_list_set = chain(mentor_list, administrator_list)
        for user in user_list_set:
            Notification.add_new_notification(
                notification_type=notification_type,
                sender=instance.user,
                questionanswer=instance.question,
                recipient=user
            )
        if instance.user != instance.question.user:
            Notification.add_new_notification(
                notification_type=notification_type,
                sender=instance.user,
                questionanswer=instance.question,
                recipient=instance.question.user
            )


@receiver(post_save, sender=QuestionAnswerFlag)
def generate_flag_notification(sender, instance, **kwargs):
    if instance.is_delete is True:
        notification_type = 7
        Notification.add_new_notification(
            notification_type=notification_type,
            sender=instance.user,
            questionanswer=instance.question,
            recipient=instance.user
        )
    else:
        notification_type = 5
    QuestionAnswerFlag.flag_notification(
        notification_type=notification_type,
        instance=instance
    )
