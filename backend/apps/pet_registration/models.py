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
    lost_date = models.DateField(default=timezone.now, verbose_name='Data de Perda')  # Corrigido: removido .date()
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
    PET_SIZE_CHOICES = [
        ('filhote', 'Filhote'),
        ('adulto', 'Adulto'),
        ('idoso', 'Idoso'),
    ]
    SPECIES_CHOICES = [('cat', 'Gato'), ('dog', 'Cachorro')]



    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, verbose_name='Espécie')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='adoption_pets', verbose_name='Dono')
    status = models.CharField(max_length=20, default='adoption', editable=False, verbose_name='Status')
    relationship_with_pet = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, verbose_name='Relação com o Pet')
    pet_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome do Pet')
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, verbose_name='Espécie')
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

class BreedingPet(models.Model):
    YES_NO_CHOICES = [('yes', 'Sim'), ('no', 'Não')]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='breeding_pets', verbose_name='Dono')
    status = models.CharField(max_length=20, default='breeding', editable=False, verbose_name='Status')
    pet_name = models.CharField(max_length=100, verbose_name='Nome do Pet')
    approximate_age = models.CharField(max_length=50, verbose_name='Idade Aproximada')
    is_neutered = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Castrado')
    approximate_weight = models.CharField(max_length=50, blank=True, null=True, verbose_name='Peso Aproximado')
    is_vaccinated = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Vacinado')
    health_issues = models.TextField(blank=True, null=True, help_text="Problemas de saúde ou necessidades especiais", verbose_name='Problemas de Saúde')
    has_pedigree = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Possui Pedigree')
    pedigree_details = models.TextField(blank=True, null=True, help_text="Detalhes do pedigree ou registro", verbose_name='Detalhes do Pedigree')
    has_bred_before = models.CharField(max_length=10, choices=YES_NO_CHOICES, verbose_name='Já Cruzou Antes')
    breeding_history = models.TextField(blank=True, null=True, help_text="Detalhes de cruzamentos anteriores", verbose_name='Histórico de Cruzamento')
    breeding_reason = models.TextField(help_text="Motivo do cruzamento (ex: reprodução de raça pura, melhoria genética)", verbose_name='Motivo do Cruzamento')
    puppy_preferences = models.TextField(blank=True, null=True, help_text="Interesse em filhotes específicos (quantidade, sexo, etc.)", verbose_name='Preferências de Filhotes')
    cost_sharing = models.TextField(blank=True, null=True, help_text="Disposição para compartilhar custos (exames, cuidados pós-parto)", verbose_name='Divisão de Custos')
    location = models.CharField(max_length=255, help_text="Endereço onde o pet está localizado", verbose_name='Localização')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    photo_1 = models.ImageField(upload_to='breeding_pets/', blank=True, null=True, verbose_name='Foto 1')
    photo_2 = models.ImageField(upload_to='breeding_pets/', blank=True, null=True, verbose_name='Foto 2')
    photo_3 = models.ImageField(upload_to='breeding_pets/', blank=True, null=True, verbose_name='Foto 3')
    terms_accepted = models.BooleanField(default=False, verbose_name='Termos Aceitos')
    privacy_policy_accepted = models.BooleanField(default=False, verbose_name='Privacidade Aceita')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return f"{self.pet_name} (Reprodução)"

    class Meta:
        verbose_name = 'Pet para Reprodução'
        verbose_name_plural = 'Pets para Reprodução'