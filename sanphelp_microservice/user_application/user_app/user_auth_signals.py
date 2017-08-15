from django.db.models.signals import post_save
from django.dispatch import receiver

from user_app.models import User


@receiver(post_save, sender=User)
def create_username(sender, instance=None,
                    created=False, **kwargs):
    """
    When a new user is created this fuctions creates a
    asociated username for newly created user
    """
    if created:
        if instance.phone_number:
            instance.username = instance.phone_number + instance.email
        else:
            instance.username = instance.email
        instance.save()
