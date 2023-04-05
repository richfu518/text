from django.apps import AppConfig


class AssetManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "asset_management"

    def ready(self):
        from . import signals