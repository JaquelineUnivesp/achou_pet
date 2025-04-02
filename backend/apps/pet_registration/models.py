from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class LostPet(models.Model):
    STATUS_CHOICES = [('lost', 'Perdido'), ('found', 'Encontrado')]
    SPECIES_CHOICES = [('cat', 'Gato'), ('dog', 'Cachorro')]
    SIZE_CHOICES = [('small', 'Pequeno'), ('medium', 'Médio'), ('large', 'Grande')]
    SEX_CHOICES = [('male', 'Macho'), ('female', 'Fêmea')]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lost_pets', verbose_name='Usuário')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost', verbose_name='Status')
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, verbose_name='Espécie')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome')
    notification_phone = models.CharField(max_length=15, help_text="Telefone para contato", verbose_name='Telefone de Notificação')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name='Tamanho')
    breed = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raça')
    color = models.CharField(max_length=100, verbose_name='Cor')
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, verbose_name='Sexo')
    lost_date = models.DateField(default=timezone.now, verbose_name='Data de Perda')
    lost_location = models.CharField(max_length=255, help_text="Endereço onde o pet foi perdido", verbose_name='Local de Perda')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    details = models.TextField(blank=True, null=True, verbose_name='Detalhes')
    photo1 = models.ImageField(upload_to='lost_pets/', blank=True, null=True, verbose_name='Foto 1')
    photo2 = models.ImageField(upload_to='lost_pets/', blank=True, null=True, verbose_name='Foto 2')
    photo3 = models.ImageField(upload_to='lost_pets/', blank=True, null=True, verbose_name='Foto 3')
    terms_accepted = models.BooleanField(default=False, verbose_name='Termos Aceitos')
    privacy_accepted = models.BooleanField(default=False, verbose_name='Privacidade Aceita')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return f"{self.name or 'Pet sem nome'} - {self.get_status_display()} por {self.user.email}"

    class Meta:
        verbose_name = 'Pet Perdido'
        verbose_name_plural = 'Pets Perdidos'

class PetAdoption(models.Model):
    RELATIONSHIP_CHOICES = [
        ('owner', 'Dono'),
        ('temporary_caretaker', 'Cuidador Temporário'),
        ('rescuer', 'Responsável pelo Resgate'),
    ]
    YES_NO_CHOICES = [('yes', 'Sim'), ('no', 'Não')]
    SOCIABILITY_CHOICES = [('yes', 'Sim'), ('no', 'Não'), ('sometimes', 'Às Vezes')]
    PET_SIZE_CHOICES = [('filhote', 'Filhote'), ('adulto', 'Adulto'), ('idoso', 'Idoso')]
    SPECIES_CHOICES = [('cat', 'Gato'), ('dog', 'Cachorro')]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='adoption_pets', verbose_name='Dono')
    status = models.CharField(max_length=20, default='adoption', editable=False, verbose_name='Status')
    relationship_with_pet = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, verbose_name='Relação com o Pet')
    pet_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome do Pet')
    species = models.CharField(
        max_length=10,
        choices=SPECIES_CHOICES,
        verbose_name='Espécie',
        blank=True,
        null=True  # Mantido null=True para evitar o erro de migração
    )
    sex = models.CharField(max_length=6, choices=[('macho', 'Macho'), ('fêmea', 'Fêmea')], null=True, blank=True, verbose_name='Sexo')
    breed = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raça')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cor')
    approximate_age = models.CharField(max_length=50, verbose_name='Idade Aproximada')
    is_neutered = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Castrado')
    approximate_weight = models.CharField(max_length=50, blank=True, null=True, verbose_name='Peso Aproximado')
    is_vaccinated = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Vacinado')
    health_issues = models.TextField(blank=True, null=True, help_text="Problemas de saúde ou necessidades especiais", verbose_name='Problemas de Saúde')
    sociable_with_animals = models.CharField(max_length=20, choices=SOCIABILITY_CHOICES, verbose_name='Sociável com Animais')
    sociable_with_children = models.CharField(max_length=20, choices=SOCIABILITY_CHOICES, verbose_name='Sociável com Crianças')
    sociable_with_strangers = models.CharField(max_length=20, choices=SOCIABILITY_CHOICES, verbose_name='Sociável com Estranhos')
    behavior = models.CharField(max_length=100, help_text="Ex: Medroso, Agitado, Calmo, etc.", verbose_name='Comportamento')
    observations = models.TextField(blank=True, null=True, help_text="Observações ou cuidados especiais", verbose_name='Observações')
    location = models.CharField(max_length=255, help_text="Endereço onde o pet está localizado", verbose_name='Localização')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    photo_1 = models.ImageField(upload_to='adoption_pets/', blank=True, null=True, verbose_name='Foto 1')
    photo_2 = models.ImageField(upload_to='adoption_pets/', blank=True, null=True, verbose_name='Foto 2')
    photo_3 = models.ImageField(upload_to='adoption_pets/', blank=True, null=True, verbose_name='Foto 3')
    terms_accepted = models.BooleanField(default=False, verbose_name='Termos Aceitos')
    privacy_policy_accepted = models.BooleanField(default=False, verbose_name='Privacidade Aceita')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    phone_for_notifications = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone para Notificações')
    size_by_age = models.CharField(max_length=7, choices=PET_SIZE_CHOICES, null=True, blank=True, verbose_name='Tamanho por Idade')

    def __str__(self):
        return f"{self.pet_name or 'Pet sem nome'} (Para Adoção)"

    class Meta:
        verbose_name = 'Pet para Adoção'
        verbose_name_plural = 'Pets para Adoção'

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class BreedingPet(models.Model):
    YES_NO_CHOICES = [('yes', 'Sim'), ('no', 'Não')]
    SPECIES_CHOICES = [('dog', 'Cachorro'), ('cat', 'Gato')]
    SEX_CHOICES = [('macho', 'Macho'), ('fêmea', 'Fêmea')]
    SIZE_BY_AGE_CHOICES = [('filhote', 'Filhote'), ('adulto', 'Adulto'), ('idoso', 'Idoso')]

    # Relacionamento com o usuário
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='breeding_pets',
        verbose_name='Dono'
    )

    # Informações básicas do pet
    pet_name = models.CharField(max_length=100, verbose_name="Nome do Pet", blank=True, null=True)
    species = models.CharField(
        max_length=10,  # Alinhado com LostPet e PetAdoption
        choices=SPECIES_CHOICES,
        verbose_name="Espécie",
        blank=True,
        null=True  # Mantido opcional, ajuste para blank=False se quiser obrigatório
    )
    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        verbose_name="Sexo",
        blank=True,
        null=True  # Mantido opcional, ajuste para blank=False se quiser obrigatório
    )
    size_by_age = models.CharField(
        max_length=20,
        choices=SIZE_BY_AGE_CHOICES,
        verbose_name="Tamanho por Idade",
        blank=True,
        null=True  # Mantido opcional
    )
    breed = models.CharField(
        max_length=100,
        verbose_name="Raça",
        blank=True,
        null=True  # Mantido opcional, ajuste para blank=False se quiser obrigatório
    )
    color = models.CharField(
        max_length=100,  # Aumentado para alinhar com LostPet
        verbose_name="Cor",
        blank=True,
        null=True  # Mantido opcional, ajuste para blank=False se quiser obrigatório
    )
    approximate_age = models.CharField(
        max_length=50,
        verbose_name="Idade Aproximada",
        blank=True,
        null=True
    )
    approximate_weight = models.CharField(
        max_length=50,
        verbose_name="Peso Aproximado",
        blank=True,
        null=True
    )

    # Saúde e características
    is_neutered = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Castrado?",
        blank=True,
        null=True
    )
    is_vaccinated = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Vacinado?",
        blank=True,
        null=True
    )
    has_pedigree = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Possui Pedigree?",
        blank=True,
        null=True
    )
    has_bred_before = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Já Cruzou Antes?",
        blank=True,
        null=True
    )
    health_issues = models.TextField(
        verbose_name="Problemas de Saúde",
        blank=True,
        null=True
    )

    # Detalhes de reprodução
    pedigree_details = models.TextField(
        verbose_name="Detalhes do Pedigree",
        blank=True,
        null=True
    )
    breeding_history = models.TextField(
        verbose_name="Histórico de Cruzamento",
        blank=True,
        null=True
    )
    breeding_reason = models.TextField(
        verbose_name="Motivo do Cruzamento",
        blank=True,
        null=True  # Ajuste para blank=False se quiser obrigatório
    )
    puppy_preferences = models.TextField(
        verbose_name="Preferências de Filhotes",
        blank=True,
        null=True
    )
    cost_sharing = models.CharField(
        max_length=100,  # Alterado de TextField para CharField para consistência
        verbose_name="Divisão de Custos",
        blank=True,
        null=True
    )

    # Contato
    phone_for_notifications = models.CharField(
        max_length=15,
        verbose_name="Telefone para Notificações",
        blank=True,
        null=True  # Mantido opcional, ajuste para blank=False se quiser obrigatório
    )

    # Fotos
    photo_1 = models.ImageField(
        upload_to='breeding_pets/photos/',
        verbose_name="Foto 1",
        blank=True,
        null=True
    )
    photo_2 = models.ImageField(
        upload_to='breeding_pets/photos/',
        verbose_name="Foto 2",
        blank=True,
        null=True
    )
    photo_3 = models.ImageField(
        upload_to='breeding_pets/photos/',
        verbose_name="Foto 3",
        blank=True,
        null=True
    )

    # Localização
    location = models.CharField(
        max_length=255,
        verbose_name="Localização",
        blank=True,
        null=True
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude"
    )

    # Termos e criação
    terms_accepted = models.BooleanField(
        default=False,
        verbose_name="Termos Aceitos"
    )
    privacy_policy_accepted = models.BooleanField(
        default=False,
        verbose_name="Política de Privacidade Aceita"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    def __str__(self):
        return self.pet_name or "Pet sem nome"

    class Meta:
        verbose_name = "Pet para Reprodução"
        verbose_name_plural = "Pets para Reprodução"