from django.apps import AppConfig


class AppwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appWeb'
    
    def ready(self):
        import appWeb.signals