from enum import Enum

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django_resized import ResizedImageField

from ppiauth.models import PPIUser


class UserProfile(models.Model):

    """
    This class creates attributes userprofile.
    """
    class UserTypes(Enum):
        """
        This class creates enum for user_type field of UserProfile.
        """
        ADMINISTRATOR = 'Administrator'
        MENTOR = 'Mentor'
        NORMAL_USER = 'Normal User'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    class Gender(Enum):
        """
        This class creates enum for gender field of UserProfile.
        """
        MALE = 'Male'
        FEMALE = 'Female'

        @classmethod
        def as_tuple(cls):
            return ((item.value, item.name.replace('_', ' ')) for item in cls)

    user = models.OneToOneField(PPIUser, primary_key=True)
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    user_type = models.CharField(blank=True, max_length=50,
                                 choices=UserTypes.as_tuple(),
                                 default=UserTypes.NORMAL_USER.value
                                 )
    designation = models.CharField(blank=True, max_length=120)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(blank=True, max_length=20,
                              choices=Gender.as_tuple())
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True,
        null=True
    )
    profile_picture_icon = ResizedImageField(
        size=[20, 20],
        quality=100,
        crop=['middle', 'center'],
        upload_to='profile_picture/',
        blank=True,
        null=True
    )
    profile_picture_thumbnail = ResizedImageField(
        size=[300, 200],
        quality=100,
        upload_to='profile_picture/',
        blank=True,
        null=True
    )
    profile_picture_macroicon = ResizedImageField(
        size=[50, 50],
        quality=100,
        crop=['middle', 'center'],
        upload_to='profile_picture/',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u''.join((self.first_name, self.last_name))

    @receiver(post_save, sender=PPIUser)
    def create_profile_for_user(sender, instance=None,
                                created=False, **kwargs):
        """
        When a new user is created this fuctions creates a userprofile
        for that particular user.
        """
        if created:
            UserProfile.objects.create(user=instance)

        if instance.is_staff:
            instance.userprofile.user_type = UserProfile.UserTypes.ADMINISTRATOR.value
            instance.userprofile.save()

    @receiver(pre_delete, sender=PPIUser)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        """
        When a user is deleted this fuctions deletes the userprofile
        of that particular user.
        """
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()
