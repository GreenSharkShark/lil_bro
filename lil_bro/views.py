import secrets
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView
from lil_bro.services import Encryptor, sha256_hash, make_link
from lil_bro.forms import SecretForm, CodePhraseForm
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
            secret.is_code_phrase = True
        else:
            secret.code_phrase = secrets.token_hex(32)

        secret.link = make_link(secret.code_phrase)
        secret.time_to_delete = timezone.now() + timezone.timedelta(minutes=secret.lifetime)

        secret.save()

        return super().form_valid(form)


class SecretRetrieveView(DetailView):
    model = Secret
    template_name = 'lil_bro/secret_retrieve.html'
    form_class = CodePhraseForm
    slug_url_kwarg = 'code_phrase'

    def get_object(self, queryset=None):
        code_phrase = self.kwargs.get(self.slug_url_kwarg)
        queryset = self.get_queryset()
        return get_object_or_404(queryset, code_phrase=code_phrase)

    def get(self, request, *args, **kwargs):
        secret = self.get_object()

        if secret.is_code_phrase:
            form = self.form_class()
            return render(request, 'lil_bro/code_phrase_form.html', {'form': form})
        else:
            secret_text = Encryptor().decrypt_text(secret.secret_text)
            secret.delete()
            return render(request, self.template_name, {'secret': secret_text})

    def post(self, request, *args, **kwargs):
        secret = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid() and sha256_hash(form.cleaned_data.get('code_phrase')) == secret.code_phrase:
            secret_text = Encryptor().decrypt_text(secret.secret_text)
            secret.delete()
            return render(request, self.template_name, {'secret': secret_text})
        else:
            return render(request, 'lil_bro/code_phrase_form.html', {'form': form, 'error': 'Неверная кодовая фраза'})
