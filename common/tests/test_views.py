import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rules.predicates import NO_VALUE

from common import views
from common.mixins import PermissionRequiredMixin


@pytest.fixture
def permission_required_mixin(fake_request):
    mixin_instance = PermissionRequiredMixin()
    mixin_instance.request = fake_request
    return mixin_instance


@pytest.mark.parametrize('perm', ["test", ["test"], ("test",), {"wrong_action": "test"}])
def test_permission_required_mixin(perm, permission_required_mixin):
    permission_required_mixin.permission_required = perm
    permissions = permission_required_mixin.get_permission_required()
    assert isinstance(permissions, tuple) or isinstance(permissions, list)


@pytest.mark.parametrize("perm, error", [
    (None, ImproperlyConfigured),
    ({1: 2}, AttributeError),
])
def test_permission_required_mixin_none_permissions(perm, error, permission_required_mixin):
    permission_required_mixin.permission_required = perm

    with pytest.raises(error):
        permission_required_mixin.get_permission_required()


def test_base_api_view_responses():
    api_view = views.APIView()
    success = api_view.success()
    fail = api_view.fail()
    assert type(success) == type(fail) == Response
    assert success.status_code == 200
    assert fail.status_code == 400
    assert success.data is fail.data is None


def test_base_api_view_permission_checking(monkeypatch, fake_request):
    api_view = views.APIView()
    api_view.kwargs = {}
    monkeypatch.setattr(fake_request.user, "has_perms", lambda *args: False)
    monkeypatch.setattr(api_view, "get_permission_required", lambda *args: "test_perm")
    with pytest.raises(PermissionDenied):
        api_view.check_permissions(fake_request)


def test_base_api_view_no_object_found(monkeypatch, fake_request):
    def mock_has_perms(perms, obj):
        assert obj == NO_VALUE
        return True

    api_view = views.APIView()
    api_view.kwargs = {}
    monkeypatch.setattr(fake_request.user, "has_perms", mock_has_perms)
    monkeypatch.setattr(api_view, "get_permission_required", lambda *args: "test_perm")
    api_view.check_permissions(fake_request)


@pytest.mark.parametrize("action, perms, expected_perms", [
    (None, None, []),
    ("get", {"get": "test"}, ("test", )),
    ("get", {"post": "test"}, ()),
])
def test_base_viewset_dict_perms(action, perms, expected_perms):
    viewset = views.ViewSet()
    viewset.action = action
    viewset.permission_required = perms
    assert viewset.get_dict_perms() == expected_perms


def test_viewset_inheritance_model():
    assert isinstance(views.APIView(), PermissionRequiredMixin)
    assert isinstance(views.ViewSet(), views.APIView)
    assert isinstance(views.ModelViewSet(), views.ViewSet)
