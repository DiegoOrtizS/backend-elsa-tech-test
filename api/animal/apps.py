from django.apps import AppConfig


class AnimalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.animal"
    label = "api_animal"
