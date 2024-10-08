from users.apps import UsersConfig
from django.urls import path
from users.views import UserRegisterView, UserLoginView
from django.contrib.auth.views import LogoutView


app_name = UsersConfig.name


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='lil_bro:secret_create'), name='logout')
]
