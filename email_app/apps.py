from django.apps import AppConfig


class MailtemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_app'

    def ready(self):
        import email_app.signals
