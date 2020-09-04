import django
django.setup()
import pytest
from django.contrib.auth.models import User



@pytest.fixture
def fake_request():
    class MockRequest:
        method = "get"
        user = User()
        authenticators = None
        successful_authenticator = None
    return MockRequest()
