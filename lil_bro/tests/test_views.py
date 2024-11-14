from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from lil_bro.models import Secret
from lil_bro.services import sha256_hash, Encryptor
from unittest.mock import patch


class SecretCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('lil_bro:secret_create')

    def test_secret_create_view(self):
        data = {
            'secret_text': 'Test secret text',
            'code_phrase': 'Test code phrase',
            'lifetime_select_field': 30,
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        secret = Secret.objects.last()
        self.assertIsNotNone(secret)

        self.assertNotEqual(secret.secret_text, 'Test secret text')

        self.assertEqual(secret.code_phrase, sha256_hash('Test code phrase'))

        self.assertTrue(secret.time_to_delete > timezone.now())

        self.assertIn('link', response.context)
        self.assertIn('pk', response.context)

    def test_secret_create_view_form_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')


class SecretRetrieveViewTest(TestCase):
    def setUp(self):
        self.secret = Secret.objects.create(
            secret_text=Encryptor().encrypt_text('Test secret text'),
            code_phrase=sha256_hash('Test code phrase'),
            lifetime=30,
        )
        self.url = reverse('lil_bro:secret_retrieve', kwargs={'pk': self.secret.pk})

    def test_secret_retrieve_view_with_code_phrase(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # We check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/code_phrase_form.html')

        # Checking the presence of the form in the context
        self.assertIn('form', response.context)

    def test_secret_retrieve_view_without_code_phrase(self):
        # Making sure that the Secret object does not have code_phrase
        self.secret.code_phrase = None
        self.secret.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # We check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/secret_retrieve.html')

        # We check that the secret has been deleted from the database
        with self.assertRaises(Secret.DoesNotExist):
            Secret.objects.get(pk=self.secret.pk)

    def test_secret_retrieve_view_post_with_valid_code_phrase(self):
        data = {'code_phrase': 'Test code phrase'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/secret_retrieve.html')

        # We check that the secret has been deleted from the database
        with self.assertRaises(Secret.DoesNotExist):
            Secret.objects.get(pk=self.secret.pk)

    def test_secret_retrieve_view_post_with_invalid_code_phrase(self):
        data = {'code_phrase': 'Invalid code phrase'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # We check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/code_phrase_form.html')

        # Checking for an error in the context
        self.assertIn('error', response.context)


class SecretDeleteViewTest(TestCase):
    def setUp(self):
        # Создаем тестовый объект Secret
        self.secret = Secret.objects.create(
            secret_text='Test secret text',
            code_phrase=sha256_hash('Test code phrase'),
            lifetime=30,
        )
        self.url = reverse('lil_bro:secret_delete', kwargs={'pk': self.secret.pk})

    def test_secret_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в ответе используется правильный шаблон
        self.assertTemplateUsed(response, 'lil_bro/secret_delete.html')

        # Проверяем, что секрет присутствует в контексте
        self.assertIn('secret', response.context)

    def test_secret_delete_view_post(self):
        response = self.client.post(self.url)

        # Проверяем, что после удаления секрета произошел редирект на 'lil_bro:secret_create'
        self.assertRedirects(response, reverse('lil_bro:secret_create'))

        # Проверяем, что секрет был удален из базы данных
        with self.assertRaises(Secret.DoesNotExist):
            Secret.objects.get(pk=self.secret.pk)


class SendReportViewTest(TestCase):
    def setUp(self):
        self.url = reverse('lil_bro:send_report')

    def test_send_report_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # We check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/send_report.html')

        # We check that the form is present in the context
        self.assertIn('form', response.context)

    @patch('lil_bro.views.send_report.delay')
    def test_send_report_view_post_valid_form(self, mock_delay):
        data = {'topic': 'Test topic', 'report': 'Test report'}
        response = self.client.post(self.url, data)

        # We check that after successfully submitting the form, there was a redirect to 'lil_bro:secret_create'
        self.assertRedirects(response, reverse('lil_bro:secret_create'))

        # We check that the send_report.delay function was called with the correct arguments
        mock_delay.assert_called_once_with(topic='Test topic', message='Test report')

    def test_send_report_view_post_invalid_form(self):
        # Testing with incorrect form data
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)

        # We check that the correct template is used in the response
        self.assertTemplateUsed(response, 'lil_bro/send_report.html')

        # Checking for errors in the form in the context
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class HowItWorksTemplateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('lil_bro:how_it_works')

    def test_how_it_works_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'lil_bro/how_it_works.html')


class SecretPlugTemplateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('lil_bro:secret_plug', kwargs={'pk': '96030cea-1a0d-4ede-ba96-5b4c8f047074'})

    def test_secret_plug_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lil_bro/secret_plug.html')
        self.assertIn('pk', response.context)
        self.assertEqual(response.context['pk'], '96030cea-1a0d-4ede-ba96-5b4c8f047074')
