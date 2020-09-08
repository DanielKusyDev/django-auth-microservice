import abc
import datetime

from django.utils.translation import gettext_lazy as _


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
