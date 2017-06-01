from django import forms
from django.contrib.auth.models import User

from account.models import UserProfile


class PPIUserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(PPIUserEditForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = 'true'

    def clean_user_type(self):
        instance = getattr(self, 'instance', None)

        if instance:
            return instance.email
        # else:
        return self.cleaned_data['email']


class PPIUserEditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'designation',
            'user_type',
            'about',
            'gender',
            'dob',
            'profile_picture',
            'first_name',
            'last_name'
        )

    def __init__(self, *args, **kwargs):
        super(PPIUserEditProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['user_type'].widget.attrs['disabled'] = 'disable'

    def clean_user_type(self):
        instance = getattr(self, 'instance', None)

        if instance:
            return instance.user_type
        # else:
        return self.cleaned_data['user_type']
