from django.core.mail.backends.console import EmailBackend as DjangoEmailBackend

from apps.mails.models import MailsConfig


class EmailBackend(DjangoEmailBackend):
    def __init__(self, *args, **kwargs):
        config = MailsConfig.get_solo()
        kwargs.setdefault('host', config.email_host)
        kwargs.setdefault('username', config.email_host_user)
        kwargs.setdefault('password', config.email_host_password)
        super().__init__(*args, **kwargs)
