from django import forms
from .models import LostPet, PetAdoption, BreedingPet
from decimal import Decimal

AGE_UNIT_CHOICES = [
    ('dias', 'Dias'), ('meses', 'Meses'), ('anos', 'Anos')
]
WEIGHT_CHOICES = [(str(i), f"{i} kg") for i in range(0, 121)]

class LostPetForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())

    class Meta:
        model = LostPet
        fields = ['species', 'status', 'name', 'notification_phone', 'size', 'breed', 'color', 'sex',
                  'coat_type', 'eye_color', 'age_value', 'age_unit', 'weight', 'lost_date', 'lost_location', 'latitude', 'longitude', 'details',
                  'photo_1', 'photo_2', 'photo_3', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'lost_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'details': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'coat_type': forms.Select(attrs={'class': 'form-select'}),
            'eye_color': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'age_unit': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.Select(choices=WEIGHT_CHOICES, attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age_value': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'notification_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'lost_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None:
            return Decimal(str(round(latitude, 6)))
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None:
            return Decimal(str(round(longitude, 6)))
        return longitude

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('terms_accepted'):
            raise forms.ValidationError("Você deve aceitar os Termos de Uso.")
        if not cleaned_data.get('privacy_accepted'):
            raise forms.ValidationError("Você deve aceitar a Política de Privacidade.")
        return cleaned_data


class AdoptionPetForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True, widget=forms.HiddenInput())

    class Meta:
        model = PetAdoption
        fields = [
            'relationship_with_pet', 'pet_name', 'species', 'sex', 'breed', 'color', 'coat_type', 'eye_color',
            'age_value', 'age_unit', 'weight', 'is_neutered', 'is_vaccinated', 'approximate_age',
            'approximate_weight', 'health_issues', 'sociable_with_animals', 'sociable_with_children',
            'sociable_with_strangers', 'behavior', 'observations', 'location', 'latitude', 'longitude',
            'photo_1', 'photo_2', 'photo_3', 'terms_accepted', 'privacy_policy_accepted',
            'phone_for_notifications', 'size_by_age'
        ]
        widgets = {
            'relationship_with_pet': forms.Select(attrs={'class': 'form-select'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'coat_type': forms.Select(attrs={'class': 'form-select'}),
            'eye_color': forms.Select(attrs={'class': 'form-select'}),
            'age_value': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'age_unit': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.Select(choices=WEIGHT_CHOICES, attrs={'class': 'form-select'}),
            'is_neutered': forms.Select(attrs={'class': 'form-select'}),
            'is_vaccinated': forms.Select(attrs={'class': 'form-select'}),
            'approximate_age': forms.TextInput(attrs={'class': 'form-control'}),
            'approximate_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'health_issues': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sociable_with_animals': forms.Select(attrs={'class': 'form-select'}),
            'sociable_with_children': forms.Select(attrs={'class': 'form-select'}),
            'sociable_with_strangers': forms.Select(attrs={'class': 'form-select'}),
            'behavior': forms.TextInput(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_for_notifications': forms.TextInput(attrs={'class': 'form-control'}),
            'size_by_age': forms.Select(attrs={'class': 'form-select'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_policy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BreedingPetForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())

    class Meta:
        model = BreedingPet
        fields = ['pet_name', 'species', 'sex', 'breed', 'color', 'coat_type', 'eye_color',
                  'age_value', 'age_unit', 'weight', 'is_neutered', 'is_vaccinated', 'has_pedigree', 'has_bred_before',
                  'health_issues', 'pedigree_details', 'breeding_history', 'breeding_reason', 'puppy_preferences',
                  'cost_sharing', 'location', 'latitude', 'longitude', 'photo_1', 'photo_2', 'photo_3',
                  'terms_accepted', 'privacy_policy_accepted', 'phone_for_notifications', 'size_by_age']
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'coat_type': forms.Select(attrs={'class': 'form-select'}),
            'eye_color': forms.Select(attrs={'class': 'form-select'}),
            'age_value': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'age_unit': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.Select(choices=WEIGHT_CHOICES, attrs={'class': 'form-select'}),
            'is_neutered': forms.Select(attrs={'class': 'form-select'}),
            'is_vaccinated': forms.Select(attrs={'class': 'form-select'}),
            'has_pedigree': forms.Select(attrs={'class': 'form-select'}),
            'has_bred_before': forms.Select(attrs={'class': 'form-select'}),
            'health_issues': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pedigree_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'breeding_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'breeding_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'puppy_preferences': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cost_sharing': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_for_notifications': forms.TextInput(attrs={'class': 'form-control'}),
            'size_by_age': forms.Select(attrs={'class': 'form-select'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_policy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }
