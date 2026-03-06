from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm, LandlordRegistrationForm

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            try:
                subject = 'Welcome to Campus Accommodation Portal!'
                html_message = render_to_string('emails/welcome_email.html', {
                    'user': user,
                    'site_url': 'http://127.0.0.1:8000',
                })
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"Welcome email sent to {user.email}")
            except Exception as e:
                print(f"Email failed: {e}")
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to CAP.')
            return redirect('core:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def landlord_register(request):
    """Special registration for landlords"""
    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Landlord registration successful!')
            return redirect('landlord:index')
    else:
        form = LandlordRegistrationForm()
    return render(request, 'accounts/landlord_register.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    context = {
        'user': user,
    }
    
    if user.user_type == 'landlord':
        # Get landlord's hostels
        from hostels.models import Hostel
        context['hostels'] = Hostel.objects.filter(landlord=user)
        return render(request, 'accounts/landlord_dashboard.html', context)
    else:
        # Get student's bookings
        from bookings.models import Booking
        context['bookings'] = Booking.objects.filter(student=user)
        return render(request, 'accounts/student_dashboard.html', context)
@login_required
def student_dashboard(request):
    """Student dashboard showing bookings and reviews"""
    
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied. Students only.')
        return redirect('core:index')
    
    # Get student's bookings
    bookings = Booking.objects.filter(student=request.user).order_by('-created_at')
    
    # Get student's reviews
    reviews = Review.objects.filter(student=request.user).order_by('-created_at')
    
    # Statistics
    total_bookings = bookings.count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    pending_bookings = bookings.filter(status='pending').count()
    total_spent = bookings.filter(status='confirmed').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    context = {
        'bookings': bookings,
        'reviews': reviews,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'pending_bookings': pending_bookings,
        'total_spent': total_spent,
    }
    
    return render(request, 'accounts/student_dashboard.html', context)