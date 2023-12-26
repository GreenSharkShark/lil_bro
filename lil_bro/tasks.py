from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from config.settings import EMAIL_HOST_USER, EMAIL_ADMIN
from .models import Secret


@shared_task
def delete_expired_secrets():
    now = timezone.now()
    expired_secrets = Secret.objects.filter(time_to_delete__lte=now)
    expired_secrets.delete()


@shared_task
def send_report(topic: str, message: str):

    send_mail(
        subject=topic,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[EMAIL_ADMIN],
        fail_silently=False
    )
