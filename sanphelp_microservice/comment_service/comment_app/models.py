from django.db import models

#Create your models here.
class Comments(models.Model):
    """
    Base class for storing Comments.
    This stores comments which is are writtten by
    user on tickets.
    """
    comment_text = models.TextField(null=True, blank=True)
    user = models.CharField(max_length=100)
    attachment = models.CharField(max_length=126,null=True, blank=True)
    ticket = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_like = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'comment'

class CommentAndVote(models.Model):
    """
    Base class for storing comment rating.
    This stores upvotes and down votes for
    each comments given by users.
    """
    user = models.CharField(max_length=100)
    comment = models.ForeignKey(Comments)

    class Meta:
        db_table = 'comment_and_vote'
