import pytest

from apps.users.models import User


def test_creating_user_with_random_password(user_data, db):
    assert not User().suspended_to
    assert not User.objects.create(**user_data).suspended_to


def test_staff_creation():
    assert False


def test_staff_listing():
    assert False


def test_superusers_listing():
    assert False


def test_non_staff_listing():
    assert False


def test_non_active_listing():
    assert False


def test_active_only_listing():
    assert False


def test_time_since_login_property():
    assert False
