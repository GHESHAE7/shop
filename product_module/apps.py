from django.apps import AppConfig


class ProductModuleConfig(AppConfig):
    name = "product_module"

    def ready(self):
        from . import signals
