import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        'username': 'TestUser',
        'password': 'TestPassword',
        'email': 'test_email@example.com',
    }


@pytest.fixture
def MockUser(monkeypatch):
    monkeypatch.setattr(User, 'save', lambda *args, **kwargs: None)
    return User


@pytest.fixture
def mock_request():
    class MockRequest:
        method = "get"
        user = User()
        authenticators = None
        successful_authenticator = None

    return MockRequest()
