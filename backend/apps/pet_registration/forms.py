from django import forms
from .models import LostPet, PetAdoption, BreedingPet
import os
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal

class LostPetForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())

    class Meta:
        model = LostPet
        fields = ['species', 'status', 'name', 'notification_phone', 'size', 'breed', 'color', 'sex',
                  'lost_date', 'lost_location', 'latitude', 'longitude', 'details',
                  'photo1', 'photo2', 'photo3', 'terms_accepted', 'privacy_accepted']
        widgets = {
            'lost_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'details': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
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
            'relationship_with_pet', 'pet_name', 'species', 'sex', 'breed', 'color', 'approximate_age',
            'is_neutered', 'approximate_weight', 'is_vaccinated', 'health_issues', 'sociable_with_animals',
            'sociable_with_children', 'sociable_with_strangers', 'behavior', 'observations', 'location', 'latitude',
            'longitude', 'photo_1', 'photo_2', 'photo_3', 'terms_accepted', 'privacy_policy_accepted',
            'phone_for_notifications', 'size_by_age'
        ]
        widgets = {
            'health_issues': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_policy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'relationship_with_pet': forms.Select(attrs={'class': 'form-select'}),
            'is_neutered': forms.Select(attrs={'class': 'form-select'}),
            'is_vaccinated': forms.Select(attrs={'class': 'form-select'}),
            'sociable_with_animals': forms.Select(attrs={'class': 'form-select'}),
            'sociable_with_children': forms.Select(attrs={'class': 'form-select'}),
            'sociable_with_strangers': forms.Select(attrs={'class': 'form-select'}),
            'behavior': forms.TextInput(attrs={'class': 'form-control'}),
            'approximate_age': forms.TextInput(attrs={'class': 'form-control'}),
            'approximate_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_for_notifications': forms.TextInput(attrs={'class': 'form-control'}),
            'size_by_age': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is None:
            raise forms.ValidationError("A latitude é obrigatória.")
        return Decimal(str(round(latitude, 6)))

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is None:
            raise forms.ValidationError("A longitude é obrigatória.")
        return Decimal(str(round(longitude, 6)))

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('terms_accepted'):
            raise forms.ValidationError("Você deve aceitar os Termos de Uso.")
        if not cleaned_data.get('privacy_policy_accepted'):
            raise forms.ValidationError("Você deve aceitar a Política de Privacidade.")
        return cleaned_data

class BreedingPetForm(forms.ModelForm):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())

    class Meta:
        model = BreedingPet
        fields = ['pet_name', 'approximate_age', 'is_neutered', 'approximate_weight', 'is_vaccinated',
                  'health_issues', 'has_pedigree', 'pedigree_details', 'has_bred_before', 'breeding_history',
                  'breeding_reason', 'puppy_preferences', 'cost_sharing', 'location', 'latitude', 'longitude',
                  'photo_1', 'photo_2', 'photo_3', 'terms_accepted', 'privacy_policy_accepted']
        widgets = {
            'health_issues': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pedigree_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'breeding_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'breeding_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'puppy_preferences': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cost_sharing': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_policy_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_neutered': forms.Select(attrs={'class': 'form-select'}),
            'is_vaccinated': forms.Select(attrs={'class': 'form-select'}),
            'has_pedigree': forms.Select(attrs={'class': 'form-select'}),
            'has_bred_before': forms.Select(attrs={'class': 'form-select'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'approximate_age': forms.TextInput(attrs={'class': 'form-control'}),
            'approximate_weight': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
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
        if not cleaned_data.get('privacy_policy_accepted'):
            raise forms.ValidationError("Você deve aceitar a Política de Privacidade.")
        return cleaned_data