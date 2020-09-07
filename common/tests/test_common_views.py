import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rules.predicates import NO_VALUE

from common import views


@pytest.mark.parametrize('perm', ["test", ["test"], ("test",), {"wrong_action": "test"}])
def test_permission_required_mixin(perm, mock_request):
    api_view = views.APIView()
    api_view.request = mock_request
    api_view.permission_required = perm
    permissions = api_view.get_permission_required()
    assert isinstance(permissions, tuple) or isinstance(permissions, list)


@pytest.mark.parametrize("perm, error", [
    (None, ImproperlyConfigured),
    ({1: 2}, AttributeError),
])
def test_api_required_permissions(perm, error, mock_request):
    api_view = views.APIView()
    api_view.request = mock_request
    api_view.permission_required = perm

    with pytest.raises(error):
        api_view.get_permission_required()


def test_base_api_view_responses():
    api_view = views.APIView()
    success = api_view.success()
    fail = api_view.fail()
    assert type(success) == type(fail) == Response
    assert success.status_code == 200
    assert fail.status_code == 400
    assert success.data is fail.data is None


def test_base_api_view_permission_checking(monkeypatch, mock_request):
    api_view = views.APIView()
    api_view.kwargs = {}
    monkeypatch.setattr(mock_request.user, "has_perms", lambda *args: False)
    monkeypatch.setattr(api_view, "get_permission_required", lambda *args: "test_perm")
    with pytest.raises(PermissionDenied):
        api_view.check_permissions(mock_request)


def test_base_api_view_no_object_found(monkeypatch, mock_request):
    def mock_has_perms(perms, obj):
        assert obj == NO_VALUE
        return True

    api_view = views.APIView()
    api_view.kwargs = {}
    monkeypatch.setattr(mock_request.user, "has_perms", mock_has_perms)
    monkeypatch.setattr(api_view, "get_permission_required", lambda *args: "test_perm")
    api_view.check_permissions(mock_request)


@pytest.mark.parametrize("action, perms, expected_perms", [
    (None, None, []),
    ("list", {"list": "test"}, ("test",)),
    ("list", {"create": "test"}, ()),
])
def test_base_viewset_dict_perms(action, perms, expected_perms):
    viewset = views.ViewSet()
    viewset.action = action
    viewset.permission_required = perms
    assert viewset.get_dict_perms() == expected_perms


def test_viewset_inheritance_model():
    assert isinstance(views.ViewSet(), views.APIView)
    assert isinstance(views.ModelViewSet(), views.ViewSet)
