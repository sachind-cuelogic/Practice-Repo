from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from ppiauth.forms import PPIAuthenticationForm


class PPIAuthLoginMiddleware(object):

    def process_request(self, request):
        """
        Completes the authentication using the AuthenticationForm.
        """
        if request.method == "POST" and ('ppi_auth_login' in request.POST):
            form = PPIAuthenticationForm(request, data=request.POST)

            if form.is_valid():
                auth_login(request, form.get_user())
                # TODO(sameet): redirect to the dashboard once implemented
                return redirect(reverse('core_index'))

            response = redirect(request.get_full_path())
            # else, invalid form, send the form errors as messages
            for field, error_list in form.errors.items():
                if field == '__all__':
                    field = _('Error')

                for error in error_list:
                    message_text = "%s: %s" % (field.capitalize(),
                                               strip_tags(error))
                    if "active" in message_text:
                        response.set_cookie('verification_email', form.get_user())
                        response.cookies['verification_email']['expires'] = 10
                        message_text = \
                            "Your email is not yet verified. Please \
                            <a href=\"/auth/registration/resend/activation/key/\">Click here</a>\
                            to send Activation Link"
                    messages.error(request, message_text)

            # redirect to the same link again to avoid form resubmissions
            return response

        else:
            form = PPIAuthenticationForm(request)

        # attach it to the request for further use
        request.login_form = form
