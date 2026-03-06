from django.shortcuts import render, redirect
from django.contrib import messages

def landlord_page(request):
    """Landlord registration page"""
    return render(request, 'landlord/index.html')

def landlord_register(request):
    """Process landlord registration"""
    if request.method == 'POST':
        # Process form data
        messages.success(request, 'Registration successful! Your hostel will be reviewed.')
        return redirect('landlord:index')
    return redirect('landlord:index')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from bookings.models import Booking
from hostels.models import Hostel, Review
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
    """Landlord dashboard showing statistics and management"""
    
    if request.user.user_type != 'landlord':
        messages.error(request, 'Access denied. Landlords only.')
        return redirect('core:index')
    
    # Get landlord's hostels
    hostels = Hostel.objects.filter(landlord=request.user)
    
    # Get all bookings for these hostels
    bookings = Booking.objects.filter(hostel__in=hostels)
    
    # Calculate statistics
    total_hostels = hostels.count()
    total_rooms = hostels.aggregate(Sum('total_rooms'))['total_rooms__sum'] or 0
    occupied_rooms = hostels.aggregate(Sum('occupied_rooms'))['occupied_rooms__sum'] or 0
    total_bookings = bookings.count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    total_revenue = bookings.filter(status='confirmed').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Recent bookings (last 10)
    recent_bookings = bookings.order_by('-created_at')[:10]
    
    # Monthly revenue for chart
    last_6_months = []
    revenue_data = []
    for i in range(5, -1, -1):
        month = timezone.now() - timedelta(days=30*i)
        month_name = month.strftime('%b')
        last_6_months.append(month_name)
        
        month_revenue = bookings.filter(
            status='confirmed',
            created_at__month=month.month,
            created_at__year=month.year
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        revenue_data.append(float(month_revenue))
    
    # Occupancy rate
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Average rating
    avg_rating = Review.objects.filter(hostel__in=hostels).aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'hostels': hostels,
        'total_hostels': total_hostels,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': total_rooms - occupied_rooms,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'occupancy_rate': round(occupancy_rate, 1),
        'avg_rating': round(avg_rating, 1),
        'last_6_months': last_6_months,
        'revenue_data': revenue_data,
    }
    
    return render(request, 'landlord/dashboard.html', context)

@login_required
def manage_hostel(request, hostel_id):
    """Manage individual hostel"""
    hostel = get_object_or_404(Hostel, id=hostel_id, landlord=request.user)
    
    if request.method == 'POST':
        # Update hostel details
        hostel.name = request.POST.get('name')
        hostel.price_per_semester = request.POST.get('price')
        hostel.description = request.POST.get('description')
        hostel.save()
        messages.success(request, 'Hostel updated successfully!')
        return redirect('landlord:dashboard')
    
    return render(request, 'landlord/manage_hostel.html', {'hostel': hostel})
@login_required
def manage_hostel(request, hostel_id):
    """Manage individual hostel"""
    hostel = get_object_or_404(Hostel, id=hostel_id, landlord=request.user)
    
    if request.method == 'POST':
        # Update hostel details
        hostel.name = request.POST.get('name')
        hostel.hostel_type = request.POST.get('hostel_type')
        hostel.campus = request.POST.get('campus')
        hostel.village = request.POST.get('location')
        hostel.price_per_semester = request.POST.get('price')
        hostel.total_rooms = request.POST.get('total_rooms')
        hostel.description = request.POST.get('description')
        hostel.contact_phone = request.POST.get('contact_phone')
        hostel.save()
        
        messages.success(request, 'Hostel updated successfully!')
        return redirect('landlord:dashboard')
    
    return render(request, 'landlord/manage_hostel.html', {'hostel': hostel})