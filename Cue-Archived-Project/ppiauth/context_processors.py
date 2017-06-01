from ppiauth.forms import PPIAuthenticationForm

def login_form(request):
    """
    Adds the authentication form to the context for all templates 
    since the login functionality is needed on all pages
    """
    if (request.login_form is None):
        login_form = PPIAuthenticationForm(request)
    else:
        login_form = request.login_form

    return {'login_form': login_form}
