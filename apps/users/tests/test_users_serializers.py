import pytest
from django.contrib.auth.hashers import check_password

from apps.users import serializers, models


@pytest.mark.django_db
def test_valid_registration(user_data, MockUser, monkeypatch):
    user_data["password2"] = user_data["password"]
    serializer_class = serializers.UserSerializer
    monkeypatch.setattr(serializer_class.Meta, 'model', MockUser)

    serializer = serializer_class(data=user_data)
    assert serializer.is_valid()

    user = serializer.save()
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert check_password(user_data["password"], user.password)


@pytest.mark.django_db
def test_password2_validation(user_data):
    serializer = serializers.UserSerializer(data=user_data)
    assert not serializer.is_valid()
    assert 'password2' in serializer.errors

    user_data['password2'] = user_data['password'] + 'wrongwrong'
    serializer = serializers.UserSerializer(data=user_data)
    assert not serializer.is_valid()
    assert 'password2' in serializer.errors


def test_user_serialization(user_data, MockUser):
    user = MockUser.objects.create_user(**user_data)
    serialized_data = serializers.UserSerializer(instance=user).data
    assert serialized_data['username'] == user.username
    assert serialized_data['email'] == user.email
    assert not serialized_data.get('password')
    assert not serialized_data.get('password2')


def test_change_password_serializer_validation():
    pass
