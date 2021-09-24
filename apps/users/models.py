from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from apps.users.services import TimeSinceLoginService
from common import time_as_dict


class UserManager(DjangoUserManager):
    use_in_migrations = True

    def create_user_with_random_password(self, username, email, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        if "password" in kwargs.keys():
            del kwargs["password"]
        password = self.make_random_password()
        return self._create_user(
            username=username, email=email, password=password, **kwargs
        )

    def create_staff(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff must have is_staff=True.")
        if extra_fields.get("is_superuser") is True:
            raise ValueError("Superuser must NOT have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def staff(self):
        return self.filter(is_staff=True)

    def superusers(self):
        return self.filter(is_superuser=True)

    def non_staff(self):
        return self.exclude(is_staff=True).exclude(is_superuser=True)

    def active_only(self):
        return self.filter(is_active=True)

    def not_active_only(self):
        return self.filter(is_active=False)


class User(AbstractUser):
    suspended_to = models.DateTimeField(
        verbose_name=_("suspended to"), null=True, blank=True
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    objects = UserManager()

    @cached_property
    def time_since_login(self):
        if self.last_login is None:
            return "-"
        else:
            time = time_as_dict(timezone.now() - self.last_login)
            return TimeSinceLoginService(self.last_login, time).get_last_login()
