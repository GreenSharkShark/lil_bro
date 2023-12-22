from celery import shared_task
from django.utils import timezone
from .models import Secret


@shared_task
def delete_expired_secrets():
    now = timezone.now()
    expired_secrets = Secret.objects.filter(time_to_delete__lte=now)
    expired_secrets.delete()
