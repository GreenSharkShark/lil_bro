from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm, Form, CharField, ChoiceField, Textarea
from django.forms.utils import ErrorList

from lil_bro.models import Secret


class SecretForm(ModelForm):
    """A form to creating Secret model's object """

    LIFETIME_CHOICES = [
        (30, '30 minutes'),
        (60, '1 hour'),
        (1440, '24 hours'),
        (4320, '3 days'),
    ]
    lifetime_select_field = ChoiceField(choices=LIFETIME_CHOICES, label='Set the lifetime')

    class Meta:
        model = Secret
        fields = ['secret_text', 'code_phrase', 'lifetime_select_field']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and request.user.is_authenticated:
            self.fields['lifetime_select_field'].choices += [(1, 'Unlimited')]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.lifetime = self.cleaned_data.get('lifetime_select_field')
        if commit:
            instance.save()
        return instance


class CodePhraseForm(Form):
    code_phrase = CharField(label='Code Phrase', max_length=100)


class ReportForm(Form):
    topic = CharField(label='Topic', max_length=100)
    report = CharField(label='Problem', widget=Textarea)
