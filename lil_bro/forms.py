from django.forms import ModelForm
from lil_bro.models import Secret


class SecretForm(ModelForm):
    """A form to creating Secret model's object"""

    class Meta:
        model = Secret
        fields = ['secret_text', 'code_phrase', 'lifetime']
