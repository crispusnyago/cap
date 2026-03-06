from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    phone_number = PhoneNumberField(region='UG', required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone_number', 'gender', 'occupation', 'nationality', 
                 'id_type', 'id_number', 'district', 'county', 'sub_county')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    """Form for editing user profile"""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 
                 'gender', 'occupation', 'nationality', 'district', 
                 'county', 'sub_county')

class LandlordRegistrationForm(UserCreationForm):
    """Specialized form for landlord registration"""
    phone_number = PhoneNumberField(region='UG')
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',
                 'gender', 'occupation', 'nationality', 'id_type', 'id_number',
                 'district', 'county', 'sub_county')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'landlord'
        if commit:
            user.save()
        return user
