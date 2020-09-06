from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from .mixins import PermissionRequiredMixin


class APIView(PermissionRequiredMixin, GenericAPIView):

    def check_permissions(self, request):
        self.request = request
        return self.has_permission()

    @classmethod
    def success(cls, status=200, data=None):
        return Response(status=status, data=data)

    @classmethod
    def fail(cls, status=400, errors=None):
        if errors:
            errors = {"errors": errors}
        return Response(status=status, data=errors)


class ViewSet(ViewSetMixin, APIView):
    def get_dict_perms(self):
        if self.action:
            perms = {key.lower(): val for key, val in self.permission_required.items()}
            perms = perms.get(self.action, ())
            if isinstance(perms, str):
                perms = (perms,)
            return perms
        return []


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   ViewSet):
    pass
