# backend/apps/pet_registration/apps.py
from django.apps import AppConfig

class PetRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pet_registration'  # Nome completo do aplicativo