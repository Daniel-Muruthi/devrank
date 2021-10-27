from django.apps import AppConfig


class DevawardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devawards'


    def ready(self):
        import devawards.signals
