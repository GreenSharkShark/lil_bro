from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from .forms import UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register_and_login.html'
    success_url = reverse_lazy('lil_bro:secret_create')

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = 'users/register_and_login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('lil_bro:secret_create')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'lil_bro/secret_delete.html'
    success_url = reverse_lazy('lil_bro:secret_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'user'
        return context
