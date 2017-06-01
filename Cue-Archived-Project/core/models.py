from datetime import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from django.utils.html import strip_entities, strip_tags

# Constant for maximum number of display messages on the home page
MAX_DISPLAY_MSG = 2

class HomePageConfig(models.Model):
    display_msg = models.TextField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # def display_message(self):
    #    return strip_entities(strip_tags(self.display_msg))

    def save(self, *args, **kwargs):
        homepage_msgs = HomePageConfig.objects.all()
        if self.active:
            homepage_msgs = homepage_msgs.filter(active=True).order_by('created_at')
            if homepage_msgs.count() < MAX_DISPLAY_MSG:
                self.active = True
            else:
                HomePageConfig.objects.filter(pk=homepage_msgs[0].id).update(active=False)
            super(HomePageConfig, self).save(*args, **kwargs)
        else:
            homepage_msgs_active = homepage_msgs.filter(active=True)
            if len(homepage_msgs_active) < MAX_DISPLAY_MSG:
                self.active = True
            else:
                if self in homepage_msgs:
                    homepage_msgs = homepage_msgs.filter(active=False).order_by('-created_at')
                    if len(homepage_msgs):
                        HomePageConfig.objects.filter(pk=homepage_msgs[0].id).update(active=True)
                
            super(HomePageConfig, self).save(*args, **kwargs)


@receiver(post_save, sender=HomePageConfig)
def post_save_story(sender, instance, **kwargs):
    homepage_msgs = sender.objects.all()
    if len(homepage_msgs) == MAX_DISPLAY_MSG:
        homepage_msgs = homepage_msgs.filter(active=False)
        if len(homepage_msgs):
            HomePageConfig.objects.filter(pk=homepage_msgs[0].id).update(active=True)
