from lil_bro.apps import LilBroConfig
from django.urls import path
from lil_bro.views import SecretCreateView, SecretRetrieveView, SecretDeleteView, SendReportView, \
    HowItWorksTemplateView, SecretPlugTemplateView

app_name = LilBroConfig.name


urlpatterns = [
    path('', SecretCreateView.as_view(), name='secret_create'),
    path('secret/<str:pk>/', SecretPlugTemplateView.as_view(), name='secret_plug'),
    path('secret/show/<str:pk>/', SecretRetrieveView.as_view(), name='secret_retrieve'),
    path('secret/delete/<str:pk>/', SecretDeleteView.as_view(), name='secret_delete'),
    path('send-report/', SendReportView.as_view(), name='send_report'),
    path('how-it-works/', HowItWorksTemplateView.as_view(), name='how_it_works'),
]
