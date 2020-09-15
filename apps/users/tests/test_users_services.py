import pytest
from django.core import mail
from django.test import override_settings, RequestFactory
from djmail.models import Message
from rest_framework.views import APIView

from apps.mails.models import MailsConfig
from apps.users import services


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND='djmail.backends.default.EmailBackend',
    DJMAIL_REAL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def test_sending_reset_password_email(mocker):
    service = services.ResetPasswordService()
    view = APIView.as_view()
    view.request = RequestFactory().request()
    view.request.build_absolute_uri = mocker.MagicMock(return_value='testurl')
    mock = mocker.MagicMock()
    mock.key = 'testtoken'
    mock.user.email = 'email@test.com'
    mock.email_host_user = 'test123@test.com'
    mocker.patch('apps.mails.models.MailsConfig.get_solo', return_value=mock)
    service.send_email_on_token_creation(None, view, mock)
    assert len(mail.outbox) == 1
    assert mock.key in Message.objects.first().body_html
    assert mail.outbox[0].from_email == 'test123@test.com'
