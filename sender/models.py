from django.db import models

# Create your models here.


class Mails(models.Model):
    recipient = models.EmailField(max_length=200, verbose_name='email')
    subject = models.CharField(max_length=255, verbose_name='subject')
    defer = models.SmallIntegerField(verbose_name='defer', default=0, blank=True)
    send_date = models.DateTimeField(verbose_name='send_date', default=None, blank=True)
    message = models.TextField(blank=True)
    status = models.BooleanField(default=False, verbose_name='sended')

    def __str__(self):
        return '{} to {}'.format(self.subject, self.recipient)

