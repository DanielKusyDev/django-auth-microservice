from datetime import datetime

import pytest
from django.contrib.auth.hashers import make_password
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _

from users import models


def test_user_model_default_values(user_data, MockUser):
    user = MockUser.objects.create(**user_data)
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert not user.suspended_to


def test_creating_user_with_random_password(MockUser, user_data):
    user_data["password"] = "passwd"
    user = MockUser.objects.create_user_with_random_password(**user_data)
    assert not user.is_staff
    assert not user.is_superuser
    assert make_password(user_data["password"]) != user.password


def test_staff_creation(MockUser, user_data):
    user = MockUser.objects.create_staff(**user_data)
    assert user.is_staff
    with pytest.raises(ValueError):
        MockUser.objects.create_staff(**user_data, is_staff=False)

    with pytest.raises(ValueError):
        MockUser.objects.create_staff(**user_data, is_superuser=True)

@pytest.mark.django_db
@pytest.mark.parametrize("manager_method, users_kwargs", [
    (models.User.objects.staff, [
        {"is_staff": True},
        {"is_staff": False}]),
    (models.User.objects.superusers, [
        {"is_staff": True, "is_superuser": True},
        {"is_staff": True, "is_superuser": False},
        {"is_staff": False, "is_superuser": False}]),
    (models.User.objects.non_staff, [
        {"is_staff": True},
        {"is_staff": False}]),
    (models.User.objects.active_only, [
        {"is_active": True},
        {"is_active": False}]),
    (models.User.objects.not_active_only, [
        {"is_active": True},
        {"is_active": False}]),
])
def test_manager_listing_by_status(manager_method, users_kwargs):
    models.User.objects.bulk_create([
        models.User(username=f"test_{i}", password=f"test_{i}", email=f"test_{i}@example.com", **kwargs)
        for i, kwargs in enumerate(users_kwargs)])
    assert manager_method().count() == 1


@pytest.mark.parametrize("move_to, last_login, message", [
    ("2020-07-01 12:12", "2020-07-01 12:12", _("moment")),
    ("2020-07-01 12:12", "2020-07-01 12:11", "1m"),
    ("2020-07-01 12:12", "2020-07-01 11:13", "59m"),
    ("2020-07-01 12:12", "2020-07-01 11:12", "1h"),
    ("2020-07-01 23:59", "2020-07-01 00:01", "23h"),
    ("2020-07-02 00:00", "2020-07-01 00:00", "1d"),
    ("2020-07-07 00:00", "2020-07-01 00:00", "6d"),
    ("2020-07-08 00:00", "2020-07-01 00:00", "01 July 2020"),
    ("2020-07-01 12:12", "2019-07-01 12:12", "01 July 2019"),
    ("2020-07-01 12:12", "2001-07-01 12:12", "01 July 2001"),
    ("2020-07-01 12:12", "2019-06-01 12:12", "01 June 2019"),
])
def test_time_since_login_property(freezer, MockUser, move_to, last_login, message):
    user = MockUser()
    date_format = "%Y-%m-%d %H:%M"
    freezer.move_to(datetime.strptime(move_to, date_format))
    user.last_login = datetime.strptime(last_login, date_format)
    user.last_login = datetime.replace(user.last_login, tzinfo=get_current_timezone())
    assert user.time_since_login == str(message)


def test_never_logged_in_time_since_login(MockUser):
    user = MockUser()
    assert user.time_since_login == "-"
