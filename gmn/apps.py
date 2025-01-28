from django.apps import AppConfig


class GmnConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gmn"

    def ready(self):
        import gmn.signals  # noqa
