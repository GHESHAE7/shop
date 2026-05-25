from django.apps import AppConfig


class SiteSettingModuleConfig(AppConfig):
    name = "site_setting_module"

    def ready(self):
        from . import signals