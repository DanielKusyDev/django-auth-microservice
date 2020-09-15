import pytest
from django.core import mail
from django.test import override_settings, RequestFactory
from djmail.models import Message
from rest_framework.views import APIView

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
    token = mocker.MagicMock()
    token.key = 'testtoken'
    token.user.email = 'email@test.com'
    service.send_email_on_token_creation(None, view, token)
    assert len(mail.outbox) == 1
    assert token.key in Message.objects.first().body_html
