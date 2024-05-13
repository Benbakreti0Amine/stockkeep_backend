from django.apps import AppConfig


class MagasinierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'magasinier'
    def ready(self):
        import magasinier.signals