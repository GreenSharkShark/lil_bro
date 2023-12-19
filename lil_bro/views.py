import secrets
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView
from lil_bro.services import Encryptor, sha256_hash, make_link
from lil_bro.forms import SecretForm
from lil_bro.models import Secret


class SecretCreateView(CreateView):
    model = Secret
    form_class = SecretForm
    template_name = 'lil_bro/secret_create.html'
    success_url = reverse_lazy('lil_bro:secret_create')

    def form_valid(self, form):
        secret = form.save()

        # encrypting the text
        secret.secret_text = Encryptor().encrypt_text(secret.secret_text)

        # hash the code phrase if it was set by the user
        if secret.code_phrase:
            secret.code_phrase = sha256_hash(secret.code_phrase)
        else:
            secret.code_phrase = secrets.token_hex(32)

        secret.link = make_link(secret.code_phrase)
        secret.time_to_delete = timezone.now() + timezone.timedelta(minutes=secret.lifetime)

        secret.save()

        return super().form_valid(form)


class SecretRetrieveView(DetailView):
    model = Secret
    template_name = 'lil_bro/secret_retrieve.html'


