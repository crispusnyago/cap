from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    """Extended user model for both students and landlords"""
    USER_TYPES = (
        ('student', 'Student'),
        ('landlord', 'Landlord'),
        ('admin', 'Admin'),
    )
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    ID_TYPES = (
        ('nin', 'National ID (NIN)'),
        ('passport', 'Passport'),
        ('driver', "Driver's License"),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = PhoneNumberField(region='UG', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Personal details for landlords
    occupation = models.CharField(max_length=100, blank=True)
    nationality = CountryField(blank=True)
    id_type = models.CharField(max_length=20, choices=ID_TYPES, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    
    # Location fields
    district = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    sub_county = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    
    # Verification - THIS IS THE FIELD WE NEED
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the user's identity has been verified"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()} - {self.user_type}"
        return f"{self.username} - {self.user_type}"
    
    def get_verification_status(self):
        """Helper function to check if a landlord can be verified"""
        missing = []
        if self.user_type == 'landlord':
            if not self.id_number:
                missing.append('ID number')
            if not self.phone_number:
                missing.append('Phone number')
            if not self.district:
                missing.append('District')
        return (len(missing) == 0, missing)