import fernet_fields
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class MailsConfig(SingletonModel):
    email_host = models.CharField(
        verbose_name=_("email host"),
        max_length=1024,
        default=settings.EMAIL_HOST)
    email_host_user = models.CharField(
        verbose_name=_("sender email"),
        max_length=1024,
        default=settings.EMAIL_HOST_USER)
    sender_name = models.CharField(
        verbose_name=_("sender name"),
        max_length=256,
        default=settings.EMAIL_HOST_USER)
    email_host_password = fernet_fields.EncryptedTextField(
        verbose_name=_('email sender password'),
        max_length=1024,
        default=settings.EMAIL_HOST_PASSWORD)
