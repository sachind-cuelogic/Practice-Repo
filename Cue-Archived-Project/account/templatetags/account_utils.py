import base64

from django import template

from ppiauth.models import PPIUser

register = template.Library()


@register.assignment_tag
def get_user_hash(user=None):
    """
    This method used for template tag
    it takes user id, retrives that user's email
    create its hash and returns it
    """
    email_hash = base64.b64encode(user.email)
    return email_hash
