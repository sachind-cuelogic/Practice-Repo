import base64

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from account.forms import PPIUserEditProfileForm, PPIUserEditForm
from ppiauth.models import PPIUser


@login_required
def profile_edit(request):
    complete_message = None
    user = request.user

    if request.method == 'POST':
        user_profile_form = PPIUserEditProfileForm(request.POST,
                                                   request.FILES,
                                                   instance=user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            if request.FILES.get('profile_picture'):
                user.userprofile.profile_picture_icon = request.FILES[
                    'profile_picture']
                user.userprofile.profile_picture_thumbnail = request.FILES[
                    'profile_picture']
                user.userprofile.profile_picture_macroicon = request.FILES[
                    'profile_picture']
                user.userprofile.save()
            complete_message = _("Profile stored successfully")
        else:
            complete_message = _("Error occurred. Please try again!")

    # else
    user_form = PPIUserEditForm(instance=user)
    user_profile_form = PPIUserEditProfileForm(instance=user.userprofile)

    return render(
        request,
        "account/profile_edit.html",
        {
            'user_form': user_form,
            'user_profile_form': user_profile_form,
            'user_profile': user.userprofile,
            'complete_message': complete_message
        }
    )


def profile_view(request, uidb64=None,):
    """
    this function gets hashed email, decodes it and use it for profile viewing
    """
    decoded_email = base64.b64decode(uidb64)
    user = get_object_or_404(PPIUser, email=decoded_email)
    return render(
        request,
        'account/profile_view.html',
        {'user': user, 'user_profile': user.userprofile}
    )
