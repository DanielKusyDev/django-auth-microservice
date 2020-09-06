import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_is_staff_perm(user_data):
    assert not User.objects.create(**user_data, is_staff=False).has_perm('is_staff')
