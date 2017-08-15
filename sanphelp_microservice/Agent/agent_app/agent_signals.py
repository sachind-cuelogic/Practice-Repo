from django.db.models.signals import post_save
from django.dispatch import receiver

from agent_app.models import Agent
# from user_auth.models import User


@receiver(post_save, sender=Agent)
def update_user_role(sender, instance=None,
                     created=False, **kwargs):
    """
    When an agent is created its role automatically
    becomes as a AGENT
    """
    if created:
        user_instance = instance.user
        user_instance.role = User.UserTypes.AGENT.value
        user_instance.save()
