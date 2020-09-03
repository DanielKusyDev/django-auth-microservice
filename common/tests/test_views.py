import pytest
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from common import views
from common.mixins import PermissionRequiredMixin


@pytest.fixture
def permission_required_mixin(fake_request):
    mixin_instance = PermissionRequiredMixin()
    mixin_instance.request = fake_request
    return mixin_instance


def test_permission_required_mixin_dict_perms():
    pass


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


def test_base_api_view_permission_checking():
    pass


def test_base_viewset_dict_perms():
    pass


def test_model_viewset_mixins():
    pass
