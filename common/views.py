from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rules.predicates import NO_VALUE
from rules.contrib.views import PermissionRequiredMixin as RulesPermissionRequiredMixin

from .mixins import PermissionRequiredMixin


class APIView(RulesPermissionRequiredMixin, PermissionRequiredMixin, GenericAPIView):
    lookup_url_kwarg = "pk"

    @classmethod
    def success(cls, status=200, data=None):
        return Response(status=status, data=data)

    @classmethod
    def fail(cls, status=400, errors=None):
        if errors:
            errors = {"errors": errors}
        return Response(status=status, data=errors)

    def check_permissions(self, request):
        perms = self.get_permission_required()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            obj = self.get_object()
        else:
            obj = NO_VALUE
        if not request.user.has_perms(perms, obj):
            self.permission_denied(request)


class ViewSet(ViewSetMixin, APIView):
    def get_dict_perms(self):
        if self.action:
            perms = {key.lower(): val for key, val in self.permission_required.items()}
            perms = perms.get(self.action, ())
            if isinstance(perms, str):
                perms = (perms, )
            return perms
        return []


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   ViewSet):
    pass
