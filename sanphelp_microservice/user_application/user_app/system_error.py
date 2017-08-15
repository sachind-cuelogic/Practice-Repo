import uuid

from validate_email import validate_email
from user_app import error_conf
from user_app.models import User


def check_for_login_input_error(data):
    """
    Error Handling For Login API
    """

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

    return False


def check_for_registration_input_error(data):
    """
    Error Handling For Registration API

    if email is not exist still getting that email
    email validation should be there
    """

    if not data.get('email'):
        return error_conf.EMAIL_NOT_PROVIDED

    elif not data.get('password'):
        return error_conf.PASSWORD_NOT_PROVIDED

    elif not data.get('confirm_password'):
        return error_conf.CONFIRM_PASSWORD_NOT_PROVIDED

    elif not data.get('source'):
        return error_conf.SOURCE_NOT_PROVIDED

    if data.get('email'):
        email_valid = validate_email(data.get('email'))
        if not email_valid:
            return error_conf.INVALID_EMAIL

    user=User.objects.filter(email=data.get('email'))

    if user:
        return error_conf.USER_ALREADY_EXISTS_AUDETEMI

    if data.get('source') != "USER_APP":
        return error_conf.INVALID_SOURCE_PROVIDED

    if data.get('password'):
        if len(data.get('password')) < 8:
            return error_conf.INSUFFICIENT_PASSWORD_LENGTH

    if (data.get('password') != data.get('confirm_password')):
        return error_conf.PASSWORDS_DOES_NOT_MATCH

    return False


def check_for_update_password_input_error(request):
    """
    Error Handling For Update Password API
    """

    data = request.data

    if not data.get('old_password'):
        return error_conf.OLD_PASSWORD_NOT_PROVIDED

    elif not data.get('new_password'):
        return error_conf.PASSWORD_NOT_PROVIDED

    elif not data.get('confirm_new_password'):
        return error_conf.CONFIRM_PASSWORD_NOT_PROVIDED

    if data.get('new_password'):
        if len(data.get('new_password')) < 8:
            return error_conf.INSUFFICIENT_PASSWORD_LENGTH
           
    if (data.get('new_password') != data.get('confirm_new_password')):
        return error_conf.PASSWORDS_DOES_NOT_MATCH

    if data.get('user_id'):
        user_obj = User.objects.filter(id = uuid.UUID(data.get('user_id'))) 
        if not user_obj:
            return error_conf.USER_DOESNOT_EXISTS
    else:
        return error_conf.USER_ID_NOT_PROVIDED

    if user_obj:
        user_obj = user_obj[0]   
        if not user_obj.check_password(data.get('old_password')):
            return error_conf.OLD_PASSWORD_INCORRECT

    return False
