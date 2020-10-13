import abc
import datetime

from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created


class BaseTimeSinceLoginService(abc.ABC):
    keys = []
    postfix = ""
    next_handler_class = None

    def __init__(self, last_login: datetime, time: datetime):
        self.last_login = last_login
        self.time = time

    def get_message(self):
        value = self.time[self.keys[0]]
        return f"{value}{self.postfix}"

    def next(self):
        return self.next_handler_class(self.last_login, self.time).get_last_login()

    def get_last_login(self):
        if any([self.time[key] > 0 for key in self.keys]):
            return self.get_message()
        return self.next()


class MinutesSinceLoginService(BaseTimeSinceLoginService):
    keys = ["minutes"]
    postfix = "m"

    def next(self):
        return _("moment")


class HoursSinceLoginService(BaseTimeSinceLoginService):
    keys = ["hours"]
    postfix = "h"
    next_handler_class = MinutesSinceLoginService


class DaysSinceLoginService(BaseTimeSinceLoginService):
    keys = ["days"]
    postfix = "d"
    next_handler_class = HoursSinceLoginService


class TimeSinceLoginService(BaseTimeSinceLoginService):
    keys = ["years", "weeks"]
    next_handler_class = DaysSinceLoginService

    def get_message(self):
        return self.last_login.strftime("%d %B %Y")


class ResetPasswordService:
    @staticmethod
    @receiver(reset_password_token_created)
    def send_email_on_token_creation(sender, instance, reset_password_token, *args, **kwargs):
        """
            Handles password reset tokens
            When a token is created, an e-mail needs to be sent to the user
            :param sender: View Class that sent the signal
            :param instance: View Instance that sent the signal
            :param reset_password_token: Token Model Object
            :param args:
            :param kwargs:
            :return:
            """
        pass

