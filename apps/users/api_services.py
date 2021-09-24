import logging

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class MailingApiService:
    BASE_URL = settings.MAILING_URL + settings.MAILING_BASE_PATH

    @classmethod
    def reset_password(cls, to, body):
        to = [to] if isinstance(to, str) else to
        data = {
            "to": to,
            "subject": str(_("Reset your password")),
            "content_type": "text/html",
            "body": body,
        }
        response = requests.post(url=cls.BASE_URL, json=data)
        logging.info(f"Mail response:\n {response.text}")
