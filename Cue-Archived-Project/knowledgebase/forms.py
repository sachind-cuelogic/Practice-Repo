from django import forms
from django.utils.translation import ugettext as _

from knowledgebase.models import QuestionAnswer
from account.models import UserProfile

from taggit.forms import TagField,TagWidget


class QuestionAnswerAddForm(forms.ModelForm):
    categories = forms.CharField(label=_("Category"),
                                 required=True,
                                 widget=forms.TextInput())
    topics = forms.CharField(label=_("Topic "),
                             required=True,
                             widget=forms.TextInput())
    difficulty_level = forms.ChoiceField(label=_("Difficulty"),
                                         required=True,
                                         choices=QuestionAnswer.DifficultyLevels.choices(),
                                         widget=forms.RadioSelect())
    tags = TagField(required=False, widget=forms.TextInput(attrs={'data-role': 'tagsinput'}))

    class Meta:
        model = QuestionAnswer
        fields = ('categories', 'topics', 'tags', 'difficulty_level', 'question', 'answer')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuestionAnswerAddForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        flag = False
        try:
            if instance:
                if self.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
                    pass
                else:
                    if instance.state == QuestionAnswer.QuestionAnswerState.PUBLISH or instance.state == QuestionAnswer.QuestionAnswerState.DRAFT:
                        if self.user != instance.user:
                            flag = True
                    elif instance.state == QuestionAnswer.QuestionAnswerState.SUBMIT:
                        if self.user != instance.user:
                            flag = True
                        elif self.user.userprofile.user_type == UserProfile.UserTypes.ADMINISTRATOR.value:
                            flag = True
                        else:
                            is_mentor = [self.user for i in instance.categories.all() if self.user in i.mentors.all()]
                            if is_mentor:
                                flag = True
        except AttributeError:
            pass

        if flag == True:
            self.fields['categories'].widget.attrs[
                'disabled'] = 'disable'
            self.fields['topics'].widget.attrs['disabled'] = 'disable'
            self.fields['difficulty_level'].widget.attrs[
                'disabled'] = 'disable'
            self.fields['question'].widget.attrs[
                'readonly'] = 'readonly'
            self.fields['answer'].widget.attrs['readonly'] = 'readonly'
