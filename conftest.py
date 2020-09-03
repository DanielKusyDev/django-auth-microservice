from dataclasses import dataclass

import pytest


@pytest.fixture
def fake_request():
    @dataclass
    class MockRequest:
        method: str = "get"

    return MockRequest()
