from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField

class Hostel(models.Model):
    """
    Main Hostel Model - represents a hostel building
    """
    
    HOSTEL_TYPES = (
        ('mixed', 'Mixed'),
        ('male', 'Male Only'),
        ('female', 'Female Only'),
    )
    
    # Relationship to landlord
    landlord = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='hostels',
        limit_choices_to={'user_type': 'landlord'},
        help_text="The landlord who owns this hostel"
    )
    
    # Basic Info
    name = models.CharField(max_length=200, db_index=True)
    hostel_type = models.CharField(max_length=20, choices=HOSTEL_TYPES, db_index=True)
    description = models.TextField(blank=True)
    
    # Location (for 6 campuses)
    CAMPUS_CHOICES = (
        ('main', 'Main Campus (Arts & Social Sciences)'),
        ('east', 'East Campus (Science & Technology)'),
        ('west', 'West Campus (Health Sciences)'),
        ('north', 'North Campus (Education)'),
        ('south', 'South Campus (Business & Economics)'),
        ('central', 'Central Campus (Agriculture)'),
    )
    
    campus = models.CharField(max_length=20, choices=CAMPUS_CHOICES, db_index=True)
    district = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200, blank=True)
    
    # Google Maps coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Room details
    total_rooms = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    occupied_rooms = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Contact
    contact_phone = PhoneNumberField(region='UG')
    alternative_phone = PhoneNumberField(region='UG', blank=True, null=True)
    
    # Verification
    is_verified = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campus', 'is_verified']),
            models.Index(fields=['price_per_semester']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_campus_display()}"
    
    @property
    def available_rooms(self):
        return self.total_rooms - self.occupied_rooms
    
    @property
    def is_available(self):
        return self.available_rooms > 0


class HostelImage(models.Model):
    """
    Multiple images for a hostel
    """
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_images/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.hostel.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            HostelImage.objects.filter(hostel=self.hostel, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class Facility(models.Model):
    """
    Available facilities (WiFi, Parking, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    
    def __str__(self):
        return self.name


class HostelFacility(models.Model):
    """
    Junction table connecting hostels to facilities
    """
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='facilities')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('hostel', 'facility')
    
    def __str__(self):
        return f"{self.hostel.name} - {self.facility.name}"


class Review(models.Model):
    """
    Student reviews and ratings
    """
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Add this line
    
    class Meta:
        unique_together = ('hostel', 'student')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username}'s review of {self.hostel.name}"