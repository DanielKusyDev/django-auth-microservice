# -*- encoding: utf-8 -*-

from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

from apps.djmail.models import MailsConfig


class RealEmailBackend(DjangoEmailBackend):
    def __init__(self, *args, **kwargs):
        config = MailsConfig.get_solo()
        kwargs.setdefault('host', config.email_host)
        kwargs.setdefault('username', config.email_host_user)
        kwargs.setdefault('password', config.email_host_password)
        super().__init__(*args, **kwargs)
