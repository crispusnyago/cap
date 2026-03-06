from django.shortcuts import render
from hostels.models import Hostel, Facility

def index(request):
    """
    Homepage view - shows featured hostels and campuses
    """
    # Get 6 most recent verified hostels for featured section
    featured_hostels = Hostel.objects.filter(is_verified=True)[:6]
    
    # Get all facilities for filter section
    facilities = Facility.objects.all()
    
    # Statistics for the homepage
    stats = {
        'total_hostels': Hostel.objects.filter(is_verified=True).count(),
        'total_students': 5000,  # You can make this dynamic later
        'total_landlords': 200,
        'total_campuses': 6,
    }
    
    context = {
        'featured_hostels': featured_hostels,
        'facilities': facilities,
        'stats': stats,
    }
    
    return render(request, 'core/index.html', context)


def about(request):
    """About page view"""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')