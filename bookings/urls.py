from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Booking creation URL - placeholder for now
    path('create/<int:hostel_id>/', views.create_booking, name='create'),
]
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # ... existing URLs ...
    
    # Payment URLs
    path('<int:booking_id>/payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/<int:booking_id>/status/', views.payment_status, name='payment_status'),
    
    # Webhook for payment notifications
    path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
]