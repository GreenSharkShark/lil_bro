from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Secret(models.Model):
    code_phrase = models.CharField(max_length=64, verbose_name='code_phrase', **NULLABLE)
    secret_text = models.TextField(verbose_name='secret text')
    link = models.CharField(max_length=250, verbose_name='link', **NULLABLE)
    lifetime = models.PositiveSmallIntegerField(verbose_name='lifetime')
    is_code_phrase = models.BooleanField(default=False)
    time_to_delete = models.DateTimeField(verbose_name='time to delete', **NULLABLE)

    def __str__(self):
        return f'Secret {self.pk}'

    class Meta:
        verbose_name = 'secret'
        verbose_name_plural = 'secrets'
