from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_apps.core'

    def ready(self):
        import local_apps.core.signals
