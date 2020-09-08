from contextlib import nullcontext

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import force_authenticate

from apps.users import views, serializers

User = get_user_model()


@pytest.fixture
def new_user_data():
    return {
        'username': 'newtestuser',
        'password': 'newpasswd',
        'email': 'newemail@example.com'
    }


@pytest.mark.django_db
def test_user_viewset_permissions(mock_request, user_data, new_user_data):
    user_viewset = views.UserViewSet()
    mock_request.user = User.objects.create(**user_data, is_staff=False)
    user_viewset.action = 'list'
    user_viewset.request = mock_request
    user_viewset.check_permissions(mock_request)
    updated_user = User.objects.create(**new_user_data)
    user_viewset.kwargs = {'pk': updated_user.pk}
    for method in 'update', 'partial_update':
        user_viewset.action = method
        with pytest.raises(PermissionDenied):
            user_viewset.check_permissions(mock_request)


@pytest.mark.django_db
@pytest.mark.parametrize('viewset_class, is_staff', [
    (views.UserViewSet, True),
    (views.StaffViewSet, False),
])
def test_viewsets_querysets(user_data, viewset_class, is_staff):
    user_viewset = viewset_class()
    user = User.objects.create(**user_data, is_staff=is_staff)
    queryset = user_viewset.get_queryset()
    assert queryset.count() == 0

    user.is_staff = not is_staff
    user.save()
    assert queryset.first() == user


@pytest.mark.django_db
@pytest.mark.parametrize('viewset_class, url_reverse', [
    (views.UserViewSet, 'users:users-list'),
    (views.StaffViewSet, 'users:staff-list'),
])
def test_viewsets_create(user_data, new_user_data, viewset_class, url_reverse):
    staff = User.objects.create_staff(**user_data)
    new_user_data['password2'] = new_user_data['password']
    factory = RequestFactory()
    request = factory.post(path=reverse(url_reverse), data=new_user_data)
    request.user = staff
    force_authenticate(request, staff)
    response = viewset_class.as_view({'post': 'create'})(request)
    assert 201 == response.status_code
    assert viewset_class().get_queryset().filter(username=new_user_data['username'])


@pytest.mark.parametrize('viewset_class, url_reverse, is_staff', [
    (views.UserViewSet, 'users:users-detail', False),
    (views.StaffViewSet, 'users:staff-detail', True),
])
@pytest.mark.django_db
def test_viewsets_update(user_data, viewset_class, url_reverse, is_staff):
    user = User.objects.create(**user_data, is_staff=is_staff)
    factory = RequestFactory()
    new_mail = 'anotheremail@example.com'
    user_data['email'] = new_mail

    for method in factory.put, factory.patch:
        request = method(path=reverse(url_reverse, kwargs={'pk': user.pk}),
                         data=user_data,
                         content_type='application/json')
        request.user = user
        force_authenticate(request, user)
        response = viewset_class.as_view({'put': 'update', 'patch': 'partial_update'})(request, pk=user.pk)
        assert 200 == response.status_code
        assert viewset_class().get_queryset().get(pk=user.pk).email == new_mail


@pytest.mark.django_db
def test_staff_viewset_delete(user_data):
    user = User.objects.create_staff(**user_data)
    request = RequestFactory().delete(path=reverse('users:staff-detail', kwargs={'pk': user.pk}))
    request.user = user
    force_authenticate(request, user)
    response = views.StaffViewSet.as_view({'delete': 'destroy'})(request, pk=user.pk)
    assert 204 == response.status_code
    assert not User.objects.filter(pk=user.pk)


@pytest.mark.django_db
def test_user_viewset_delete(user_data):
    user = User.objects.create_user(**user_data)
    request = RequestFactory().delete(path=reverse('users:users-detail', kwargs={'pk': user.pk}))
    request.user = user
    force_authenticate(request, user)
    response = views.UserViewSet.as_view({'delete': 'destroy'})(request, pk=user.pk)
    assert 204 == response.status_code
    assert not User.objects.filter(pk=user.pk)


@pytest.mark.django_db
@pytest.mark.parametrize('is_valid, response_status_code, exc', [
    (True, 200, ValidationError('test')),
    (False, 400, nullcontext())
])
def test_password_changing_api_view(mocker, user_data, is_valid, response_status_code, exc):
    if not is_valid:
        mocker.patch('apps.users.serializers.ChangePasswordSerializer.errors', return_value=['test error'])
    mocker.patch('apps.users.serializers.ChangePasswordSerializer.save', return_value=None)
    mocker.patch('apps.users.serializers.ChangePasswordSerializer.is_valid', return_value=is_valid)
    user = User.objects.create(**user_data)
    request = RequestFactory().put(path=reverse('users:password_change'), content_type='application/json')
    request.user = user
    force_authenticate(request, user)
    response = views.ChangePasswordAPIView.as_view()(request)
    assert response.status_code == response_status_code
    assert bool(response.data) != is_valid


@pytest.mark.django_db
def test_password_serialization(user_data):
    user = User.objects.create_user(**user_data)
    data = serializers.ChangePasswordSerializer(instance=user).data
    assert not data


@pytest.mark.django_db
@pytest.mark.parametrize('data, expected', [
    ({'old_password': 'test123!@#', 'password': 'newtest123!@#', 'password2': 'newtest123!@#'}, True),
    ({'old_password': 'test123!@#', 'password': 'test123!@#', 'password2': 'test123!@#'}, False),
    ({'password': 'test123!@#', 'password2': 'test123!@#'}, False),
    ({'old_password': 'surelywrongpassword', 'password': 'test123!@#', 'password2': 'test123!@#'}, False),
])
def test_old_password_validation_in_change_password_serializer(data, expected, user_data):
    user_data['password'] = 'test123!@#'
    user = User.objects.create_user(**user_data)
    serializer = serializers.ChangePasswordSerializer(instance=user, data=data)
    assert serializer.is_valid() == expected


def test_if_change_password_serializer_derives_from_user_serializer():
    # There are tested functionalities in UserSerializer class so all I need to do is to check if
    # ChangePasswordSerializer share those functionalities
    assert isinstance(serializers.ChangePasswordSerializer(), serializers.UserSerializer)
