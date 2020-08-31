from django.core.exceptions import ImproperlyConfigured


class PermissionRequiredMixin:
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
