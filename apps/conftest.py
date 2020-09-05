import pytest


@pytest.fixture
def user_data():
    return {
        'username': 'TestUser',
        'password': 'TestPassword',
        'email': 'TestEmail',
    }