from tinymce.widgets import TinyMCE
from django import forms
from core.models import HomePageConfig

class HomePageConfigForm(forms.ModelForm):
    display_msg = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = HomePageConfig
        fields = ('display_msg', 'active',)
