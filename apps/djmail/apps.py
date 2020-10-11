from django.apps import AppConfig


class DjMailConfig(AppConfig):
    name = 'apps.djmail'
    verbose_name = "DjMail"

    def ready(self):
        from . import signals
        super(DjMailConfig, self).ready()
