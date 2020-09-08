import pytest
from django.conf import settings

from apps.mails import models


@pytest.mark.django_db
def test_mails_config_defaults():
    config = models.MailsConfig.get_solo()
    assert config.email_host == settings.EMAIL_HOST
    assert config.email_host_user == settings.EMAIL_HOST_USER
    assert config.sender_name == settings.EMAIL_HOST_USER
    assert config.email_host_password == settings.EMAIL_HOST_PASSWORD


