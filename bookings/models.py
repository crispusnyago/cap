from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from hostels.models import Hostel

class Booking(models.Model):
    """
    Booking Model - Represents a student's room reservation
    """
    
    # Booking status options (like order stages)
    BOOKING_STATUS = (
        ('pending', 'Pending'),      # Just started, not paid
        ('confirmed', 'Confirmed'),  # Paid and confirmed
        ('cancelled', 'Cancelled'),  # Cancelled
        ('completed', 'Completed'),  # Stay is over
    )
    
    # Payment method options
    PAYMENT_METHODS = (
        ('mtn', 'MTN MoMo'),
        ('airtel', 'Airtel Money'),
        ('cash', 'Cash'),
    )
    
    # Who is booking? (Link to student user)
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # What hostel are they booking? (Link to hostel)
    hostel = models.ForeignKey(
        Hostel, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Booking dates
    check_in_date = models.DateField()   # When they move in
    check_out_date = models.DateField()  # When they move out
    
    # Payment details
    amount_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS
    )
    payment_reference = models.CharField(
        max_length=100, 
        unique=True
    )
    
    # Booking status
    status = models.CharField(
        max_length=20, 
        choices=BOOKING_STATUS, 
        default='pending'
    )
    
    # Mobile money details
    phone_number = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest bookings first
    
    def __str__(self):
        return f"Booking {self.id} - {self.student.username} - {self.hostel.name}"
    
    @property
    def is_paid(self):
        """Check if booking is paid for"""
        return self.status in ['confirmed', 'completed']


class Payment(models.Model):
    """
    Payment Model - Detailed record of each transaction
    """
    
    # Link to the booking (one booking = one payment)
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE,
        related_name='payment'
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    network = models.CharField(max_length=20, help_text="MTN or Airtel")
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    response_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id}"