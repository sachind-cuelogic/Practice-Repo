from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'user_app'

    def ready(self):
        import user_app.user_auth_signals
