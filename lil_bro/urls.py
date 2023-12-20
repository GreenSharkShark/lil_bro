from lil_bro.apps import LilBroConfig
from django.urls import path
from lil_bro.views import SecretCreateView, SecretRetrieveView

app_name = LilBroConfig.name


urlpatterns = [
    path('', SecretCreateView.as_view(), name='secret_create'),
    path('secret/<str:code_phrase>/', SecretRetrieveView.as_view(), name='secret_retrieve'),
]
