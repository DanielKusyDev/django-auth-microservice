import pytest
from django.contrib.auth.hashers import make_password

from apps.users import models


@pytest.fixture
def User(monkeypatch):
    monkeypatch.setattr(models.User, 'save', lambda *args, **kwargs: None)
    return models.User


def test_user_model_default_values(user_data, User):
    user = User.objects.create(**user_data)
    assert not user.suspended_to


def test_creating_user_with_random_password(User, user_data):
    user_data["password"] = "passwd"
    user = User.objects.create_user_with_random_password(**user_data)
    assert not user.is_staff
    assert not user.is_superuser
    assert make_password(user_data["password"]) != user.password


def test_staff_creation(User, user_data):
    user = User.objects.create_staff(**user_data)
    assert user.is_staff


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


def test_time_since_login_property(user_data):
    assert False
