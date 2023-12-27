from django.test import TestCase
from django.utils import timezone
from lil_bro.models import Secret
from lil_bro.tasks import delete_expired_secrets


class DeleteExpiredSecretsTest(TestCase):
    def test_delete_expired_secrets_task(self):
        expired_secret1 = Secret.objects.create(secret_text='f',
                                                lifetime=10,
                                                time_to_delete=timezone.now() - timezone.timedelta(minutes=10))
        expired_secret2 = Secret.objects.create(secret_text='f',
                                                lifetime=5,
                                                time_to_delete=timezone.now() - timezone.timedelta(minutes=5))

        delete_expired_secrets()

        self.assertFalse(Secret.objects.filter(pk=expired_secret1.pk).exists())
        self.assertFalse(Secret.objects.filter(pk=expired_secret2.pk).exists())
