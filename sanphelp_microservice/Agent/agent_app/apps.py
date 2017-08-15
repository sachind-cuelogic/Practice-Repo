from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'agent'

    def ready(self):
        import agent_app.agent_signals
