from django.apps import AppConfig


class MoribitModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Moribit_Module'

    def ready(self):
        import Moribit_Module.tasks


