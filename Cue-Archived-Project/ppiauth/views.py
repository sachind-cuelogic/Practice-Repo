from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from django.utils import timezone

from core.utils import generate_activation_key
from core.utils import generate_expiry_timestamp

from ppiauth.forms import PPIUserRegistrationForm
from ppiauth.models import PPIUser
from knowledgebase.views import validateurl


@require_http_methods(["GET", "POST"])
def registration(request):

    if request.method == 'POST':
        user_form = PPIUserRegistrationForm(request.POST)
        print "user_form==>",user_form
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            print "email===>",email
            activation_key = generate_activation_key(email)
            print "activation key==>",activation_key
            key_expires = generate_expiry_timestamp()
            print "key_expires==>",key_expires
            user = user_form.save(commit=False)
            user.activation_key = activation_key
            print "active suer key===>",user.activation_key
            user.key_expires = key_expires
            user.set_password(user_form.cleaned_data['password'])
            print "user pass==>",user.set_password(user_form.cleaned_data['password'])  
            
            user.save()
            print "user==>",user
            send_activation_link(activation_key, email, request)

            return redirect(reverse('ppi-auth:registration_success'))
    else:
        user_form = PPIUserRegistrationForm()

    return render(
        request,
        'ppiauth/registration.html',
        {'user_form': user_form}
    )

@validateurl
def resend_activation_key(request):
    form = PPIUserRegistrationForm()
    try:
        activation = request.META.get('HTTP_REFERER').split('/')[6]
        user = PPIUser.objects.get(activation_key=activation)

    except:
        verification_email = request.COOKIES.get('verification_email')
        user = PPIUser.objects.get(email=verification_email)

    if user is not None and not user.is_active:
        email = user.email
        activation_key = user.activation_key
        key_expires = generate_expiry_timestamp()

        user.key_expires = key_expires
        user.save()
        
        send_activation_link(activation_key, email, request)

        response = render(request,'ppiauth/resend_activation_link.html')
        response.delete_cookie('verification_email')

        return response

def send_activation_link(activation_key, email, request):
    url = reverse(
            'ppi-auth:registration_confirm',
            kwargs={'activation_key': activation_key}
        )
    print "url ==>",url

    email_subject = 'Account confirmation'
    email_body = "Hey, thanks for signing up.\n\
    To activate your account, click this link within \
    48 hours\n  http://%s%s" % (request.META['HTTP_HOST'], url)

    print "email body===>",email_body

    send_mail(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False 
    )

    print "send mail==>",send_mail

def registration_confirm(request, activation_key):
    try:
        PPIUser.objects.get(activation_key=activation_key)
        print "ppiuser activation key==>",PPIUser.objects.get(activation_key=activation_key)
        user = get_object_or_404(PPIUser, activation_key=activation_key)
        if request.user.is_authenticated():
            return render(request, 'ppiauth/confirm.html')

        if user.key_expires < timezone.now():
            return render(request, 'ppiauth/confirm_expired.html')

        user.activation_key = ""
        user.is_active = True
        user.save()
        return render(request, 'ppiauth/confirm.html')
    except:
        return render(request, 'ppiauth/account_active.html')


def registration_success(request):
    return render(request, 'ppiauth/registration_success.html')


def email_verify(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = PPIUser.objects.get(email=email)
        except PPIUser.DoesNotExist:
            return HttpResponse("Sorry!! The entered email is not registered.")
        if user.is_active:
            return HttpResponse("success")
        return HttpResponse("Sorry!! Your account is not active yet.")
    return HttpResponse("Failed")
