import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIClient, force_authenticate

from apps.users import views

User = get_user_model()


@pytest.fixture
def new_user_data():
    return {
        'username': 'newtestuser',
        'password': 'newpasswd',
        'email': 'newemail@example.com'
    }


@pytest.mark.django_db
@pytest.fixture
def staff(user_data):
    return User.objects.create_staff(**user_data)


@pytest.fixture
def user_viewset():
    viewset = views.UserViewSet()
    viewset.kwargs = {}
    return viewset


@pytest.mark.django_db
def test_user_viewset_permissions(user_viewset, mock_request, user_data):
    mock_request.user = User.objects.create(**user_data, is_staff=False)
    with pytest.raises(PermissionDenied):
        user_viewset.check_permissions(mock_request)


@pytest.mark.django_db
def test_user_viewset_queryset(user_viewset, user_data):
    user = User.objects.create(**user_data)
    assert user_viewset.get_queryset().first() == user


@pytest.mark.django_db
def test_user_viewset_create(staff, new_user_data):
    new_user_data['password2'] = new_user_data['password']
    factory = RequestFactory()
    request = factory.post(path=reverse('users:users-list'), data=new_user_data)
    request.user = staff
    force_authenticate(request, staff)
    response = views.UserViewSet.as_view({'post': 'create'})(request)
    assert 201 == response.status_code
    assert User.objects.filter(username=new_user_data['username'])


@pytest.mark.django_db
def test_user_viewset_update(staff, new_user_data):
    factory = RequestFactory()
    user = User.objects.create_user(**new_user_data)
    new_mail = 'anotheremail@example.com'
    new_user_data['email'] = new_mail
    for method in factory.put, factory.patch:
        request = method(path=reverse('users:users-details', kwargs={'pk': user.pk}), data=new_user_data)
        request.user = staff
        force_authenticate(request, staff)
        response = views.UserViewSet.as_view({'put': 'update', 'patch': 'partial_update'})(request)
        assert 201 == response.status_code
        assert User.objects.get(pk=user.pk).email == new_mail


@pytest.mark.django_db
def test_user_viewset_delete(staff, new_user_data):
    factory = RequestFactory()
    user = User.objects.create(**new_user_data)
    request = factory.delete(path=reverse('users:users-details', kwargs={'pk': user.pk}))
    request.user = staff
    force_authenticate(request, staff)
    response = views.User.as_view({'delete': 'destroy'})(request)
    assert 200 == response.status_code
    assert not User.objects.filter(pk=user.pk)
