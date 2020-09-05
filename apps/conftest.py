import pytest


@pytest.fixture(scope='session')
def user_data():
    return {
        'username': 'TestUser',
        'password': 'TestPassword',
        'email': 'TestEmail',
    }