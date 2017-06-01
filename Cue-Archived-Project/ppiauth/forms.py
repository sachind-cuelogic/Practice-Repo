from django import forms
from django.contrib.auth.forms import (AuthenticationForm,
                                       ReadOnlyPasswordHashField)
from django.utils.translation import ugettext as _

from captcha.fields import ReCaptchaField

from ppiauth.models import PPIUser


class PPIUserRegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs=
        {'placeholder':_('Password')}))
    password_repeat = forms.CharField(label=_("ConfirmPassword"),
        widget=forms.PasswordInput(attrs=
        {'placeholder':_('Repeat Password')}))
    captcha = ReCaptchaField(label=_("Captcha"))

    class Meta:
        model = PPIUser
        fields = ('email',)

    def clean_password_repeat(self):
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password_repeat

    def save(self, commit=True):
        user = super(PPIUserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.is_active = False
            user.save()
        return user

    def clean_password_repeat(self):
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError("Password don't match")
        # else
        return password_repeat


class PPIUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Password',
                                      widget=forms.PasswordInput)

    class Meta:
        model = PPIUser
        fields = ('email',)

    def clean_password_repeat(self):
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError(_("Password dont match"))
        # else
        return password_repeat

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            PPIUser.objects.get(email=email)
        except PPIUser.DoesNotExist:
            return email
        raise forms.ValidationError(_("Username already Exists"))

    def save(self, commit=True):
        user = super(PPIUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class PPIUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = PPIUser
        fields = ('email', 'password', 'is_staff', 'is_active',
                  'activation_key')

    def clean_password(self):
        return self.initial["password"]


class PPIAuthenticationForm(AuthenticationForm):
    """
    Overrides Django's authentication form to add placeholders.
    """
    username = forms.CharField(max_length=254,
                               label=_("Email"),
                               widget=forms.TextInput(
                                    attrs={'placeholder':_('Email')}))

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(
                                    attrs={'placeholder':_('Password')}))
