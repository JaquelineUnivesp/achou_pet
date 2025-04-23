from apps.pet_registration.models import LostPet

# Veja TODOS os pets cadastrados no banco de dados
LostPet.objects.all()


from django.contrib import admin
from .models import LostPet, PetAdoption, BreedingPet  # ou o que você tiver

admin.site.register(LostPet)
admin.site.register(PetAdoption)
admin.site.register(BreedingPet)
