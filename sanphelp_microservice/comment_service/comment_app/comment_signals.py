from django.db.models.signals import (pre_save,
                                      post_save,
                                      post_delete)
from django.dispatch import receiver

from comment_app.models import ( Comments,
                                 CommentAndVote,
                                )

# ###############################################################################
# # Comment Vote Post save/delete Signal
# ###############################################################################
@receiver(post_save, sender=CommentAndVote)
def increase_like_count_on_comment(sender, instance=None,
                                   created=False, **kwargs):
    """
    When a user likes a comment the total likes
    in comment automatically gets increased.
    """
    if created:
        comment_object = instance.comment
        comment_object.total_like += 1
        comment_object.save()


@receiver(post_delete, sender=CommentAndVote)
def decrease_like_count_on_comment(sender, instance=None,
                                   created=False, **kwargs):
    """
    When a user dislikes a comment the total likes
    in comment automatically gets decreased.
    """
    if instance:
        comment_object = instance.comment
        if comment_object.total_like > 1:
            comment_object.total_like -= 1
            comment_object.save()


# ###############################################################################
# # total ticket comment count Post save Signal
# ###############################################################################
@receiver(post_save, sender=Comments)
def update_comment_count_on_ticket(sender, instance=None,
                                   created=False, **kwargs):
    """
    When user comments on a ticket the comment
    count automatically gets increased.
    """
    if created:
        ticket_object = instance.ticket
        ticket_object.comment_count += 1
        ticket_object.save()

    if not instance.is_active:
        ticket_object = instance.ticket
        if ticket_object.comment_count > 1:
            ticket_object.comment_count -= 1
            ticket_object.save()
