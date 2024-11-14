from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, TemplateView, ListView
from lil_bro.services import Encryptor, sha256_hash, make_link
from lil_bro.forms import SecretForm, CodePhraseForm, ReportForm
from lil_bro.models import Secret
from lil_bro.tasks import send_report


class SecretCreateView(CreateView):
    model = Secret
    form_class = SecretForm
    template_name = 'lil_bro/secret_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        secret = form.save()

        # encrypting the text
        secret.secret_text = Encryptor().encrypt_text(secret.secret_text)

        # hash the code phrase if it was set by the user
        if secret.code_phrase:
            secret.code_phrase = sha256_hash(secret.code_phrase)

        if secret.lifetime != '1':
            secret.time_to_delete = timezone.now() + timezone.timedelta(minutes=int(secret.lifetime))

        if self.request.user.is_authenticated and secret.lifetime == '1':
            secret.created_by = self.request.user

        secret.save()

        if secret.lifetime != '1':
            link = make_link(secret.id)
        else:
            link = None

        return render(self.request, 'lil_bro/copy_link.html', {'link': link, 'pk': secret.pk})

    def get_context_data(self, **kwargs):
        """ Add model name to context to show different text in template """
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'secret'
        return context


class SecretRetrieveView(DetailView):
    model = Secret
    template_name = 'lil_bro/secret_retrieve.html'
    form_class = CodePhraseForm

    def get(self, request, *args, **kwargs):
        secret = self.get_object()

        if secret.code_phrase:
            form = self.form_class()
            return render(request, 'lil_bro/code_phrase_form.html', {'form': form})
        else:
            secret_text = Encryptor().decrypt_text(secret.secret_text)
            secret.delete()
            return render(request, self.template_name, {'secret': secret_text, 'model_name': 'secret_retrieve'})

    def post(self, request, *args, **kwargs):
        secret = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid() and sha256_hash(form.cleaned_data.get('code_phrase')) == secret.code_phrase:
            secret_text = Encryptor().decrypt_text(secret.secret_text)
            secret.delete()
            return render(request, self.template_name, {'secret': secret_text, 'model_name': 'secret_retrieve'})
        else:
            return render(request, 'lil_bro/code_phrase_form.html', {'form': form, 'error': 'Неверная кодовая фраза'})


class SavedSecretsListView(ListView):
    model = Secret
    template_name = 'lil_bro/secret_retrieve.html'

    def get_queryset(self):
        return Secret.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'secret_list'
        encryptor = Encryptor()

        for secret in context['object_list']:
            secret.secret_text = encryptor.decrypt_text(secret.secret_text)

        return context


class SecretDeleteView(DeleteView):
    model = Secret
    template_name = 'lil_bro/secret_delete.html'
    success_url = reverse_lazy('lil_bro:secret_create')


class SendReportView(View):
    template_name = 'lil_bro/send_report.html'

    def get(self, request):
        form = ReportForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data.get('topic')
            message = form.cleaned_data.get('report')
            send_report.delay(topic=topic, message=message)
            return redirect('lil_bro:secret_create')

        return render(request, self.template_name, {'form': form})


class HowItWorksTemplateView(TemplateView):
    template_name = 'lil_bro/how_it_works.html'


class SecretPlugTemplateView(TemplateView):
    template_name = 'lil_bro/secret_plug.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context
