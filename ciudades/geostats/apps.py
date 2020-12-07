from django.apps import AppConfig


class GeostatsConfig(AppConfig):
    name = 'ciudades.geostats'

    def ready(self):
        import ciudades.geostats.signals
