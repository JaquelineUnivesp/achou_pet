from django import forms
from .models import CustomUser


# Formulário de cadastro
class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'notification_phone', 'photo', 'cpf',
            'notify_chat', 'notify_pet_found', 'notify_other'
        ]
        widgets = {
            'notify_chat': forms.CheckboxInput(),
            'notify_pet_found': forms.CheckboxInput(),
            'notify_other': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem")
        return cleaned_data


# Formulário de edição de perfil
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'username', 'email',
            'notification_phone', 'photo', 'cpf',
            'notify_chat', 'notify_pet_found', 'notify_other'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notification_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'notify_chat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_pet_found': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_other': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
