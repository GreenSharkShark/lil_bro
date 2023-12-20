from django.forms import ModelForm, Form, CharField
from lil_bro.models import Secret


class SecretForm(ModelForm):
    """A form to creating Secret model's object"""

    class Meta:
        model = Secret
        fields = ['secret_text', 'code_phrase', 'lifetime']


class CodePhraseForm(Form):
    code_phrase = CharField(label='Code Phrase', max_length=100)

