from django.contrib.auth import mixins
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import BaseCreateView
from rules.predicates import NO_VALUE


class PermissionRequiredMixin(mixins.PermissionRequiredMixin):
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

    def has_permission(self):
        perms = self.get_permission_required()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            obj = self.get_object()
        else:
            obj = NO_VALUE
        return self.request.user.has_perms(perms, obj)
