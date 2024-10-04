from django.apps import AppConfig


class KitchenappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kitchenapp'

    def ready(self):
        import kitchenapp.signals
