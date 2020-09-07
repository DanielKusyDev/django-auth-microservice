from django.core.exceptions import ImproperlyConfigured
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rules.predicates import NO_VALUE


class APIView(GenericAPIView):
    permission_required = []
    lookup_url_kwarg = "pk"

    def get_dict_perms(self):
        perms = {key.lower(): val for key, val in self.permission_required.items()}
        perms = perms.get(self.request.method.lower(), ())
        return perms

    def get_permission_required(self):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        elif isinstance(self.permission_required, dict):
            perms = self.get_dict_perms()
        else:
            perms = self.permission_required
        return perms

    def check_permissions(self, request):
        perms = self.get_permission_required()
        obj = self.get_object()
        if not request.user.has_perms(perms, obj):
            self.permission_denied(request)
        super().check_permissions(request)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            queryset = self.filter_queryset(self.get_queryset())
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, obj)
            return obj
        return NO_VALUE

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
