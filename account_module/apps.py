from django.apps import AppConfig


class AccountModuleConfig(AppConfig):
    name = "account_module"

    def ready(self):
        from . import signals
