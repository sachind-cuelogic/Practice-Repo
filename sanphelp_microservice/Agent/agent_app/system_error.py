from validate_email import validate_email

from agent_app.models import Agent
from agent_app import error_conf
# from user_auth.models import User


def check_for_login_input_error(data):
    ###
    # Error Handling For Admin App Login
    ###

    if not data.get('email'):
        return error_conf.EMAIL_NOT_PROVIDED

    elif not data.get('password'):
        return error_conf.PASSWORD_NOT_PROVIDED

    elif not data.get('source'):
        return error_conf.SOURCE_NOT_PROVIDED

    if data.get('email'):
        email_valid = validate_email(data.get('email'))
        if not email_valid:
            return error_conf.INVALID_EMAIL

    if len(User.objects.filter(email=data.get('email'))) == 0:
        return error_conf.USER_DOES_NOT_EXIST

    user = User.objects.filter(email=data.get('email'))[0]

    if not user.is_active:
        return error_conf.USER_IS_INACTIVE

    if data.get('source') != 'AGENT_APP':
        return error_conf.INVALID_SOURCE_PROVIDED

    if user.role == User.UserTypes.AGENT.value:
        if not user.agent.is_admin:
            return error_conf.INVALID_USER

    if user.role == User.UserTypes.NORMAL_USER.value:
        if not user.userprofile.is_admin:
            return error_conf.INVALID_USER

    return False
