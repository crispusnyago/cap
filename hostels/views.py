from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hostel, Facility, Review
from .forms import HostelSearchForm, ReviewForm

def hostel_list(request):
    """
    Show all hostels with search and filter
    """
    hostels = Hostel.objects.filter(is_verified=True)
    
    # Get filter parameters from URL
    campus = request.GET.get('campus')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    hostel_type = request.GET.get('type')
    facilities = request.GET.getlist('facilities')
    search = request.GET.get('search')
    
    # Apply filters
    if campus and campus != 'all':
        hostels = hostels.filter(campus=campus)
    
    if min_price:
        hostels = hostels.filter(price_per_semester__gte=min_price)
    
    if max_price:
        hostels = hostels.filter(price_per_semester__lte=max_price)
    
    if hostel_type:
        hostels = hostels.filter(hostel_type=hostel_type)
    
    if facilities:
        for facility in facilities:
            hostels = hostels.filter(facilities__facility__name=facility)
    
    if search:
        hostels = hostels.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(village__icontains=search)
        )
    
    # Get all facilities for filter sidebar
    all_facilities = Facility.objects.all()
    
    # Campus choices for filter display
    campus_choices = [
        ('main', 'Main Campus'),
        ('mbale', 'Mbale Campus'),
        ('namasagali', 'Namasagali Campus'),
        ('nagongera', 'Nagongera Campus'),
        ('pallisa', 'Pallisa Campus'),
        ('arapai', 'Arapai Campus'),
    ]
    
    context = {
        'hostels': hostels,
        'facilities': all_facilities,
        'campus_choices': campus_choices,
        'total_count': hostels.count(),
    }
    
    return render(request, 'hostels/list.html', context)


def hostel_detail(request, pk):
    """
    Show single hostel details
    """
    hostel = get_object_or_404(Hostel, pk=pk, is_verified=True)
    
    # Get related data
    images = hostel.images.all()
    facilities = hostel.facilities.filter(is_available=True)
    reviews = hostel.reviews.all()
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated and request.user.user_type == 'student':
        user_review = Review.objects.filter(hostel=hostel, student=request.user).first()
    
    context = {
        'hostel': hostel,
        'images': images,
        'facilities': facilities,
        'reviews': reviews,
        'user_review': user_review,
    }
    
    return render(request, 'hostels/detail.html', context)


@login_required
def add_review(request, hostel_id):
    """
    Add or edit a review for a hostel
    """
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    if request.user.user_type != 'student':
        messages.error(request, 'Only students can leave reviews.')
        return redirect('hostels:detail', pk=hostel_id)
    
    # Check if user already reviewed
    existing_review = Review.objects.filter(hostel=hostel, student=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.hostel = hostel
            review.student = request.user
            review.save()
            
            if existing_review:
                messages.success(request, 'Your review has been updated!')
            else:
                messages.success(request, 'Thank you for your review!')
            
            return redirect('hostels:detail', pk=hostel_id)
    else:
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'hostels/review_form.html', {
        'form': form,
        'hostel': hostel,
        'is_edit': existing_review is not None
    })
from django.contrib.auth.decorators import login_required

@login_required
def hostel_create(request):
    """Create a new hostel (landlords only)"""
    if request.user.user_type != 'landlord':
        messages.error(request, 'Only landlords can create hostels.')
        return redirect('hostels:list')
    
    # Simple placeholder - you can expand this later
    messages.info(request, 'Hostel creation form coming soon!')
    return redirect('landlord:dashboard')
from django.contrib.auth.decorators import login_required

@login_required
def hostel_create(request):
    """Create a new hostel (landlords only)"""
    if request.user.user_type != 'landlord':
        messages.error(request, 'Only landlords can create hostels.')
        return redirect('hostels:list')
    
    if request.method == 'POST':
        # Create new hostel
        hostel = Hostel.objects.create(
            landlord=request.user,
            name=request.POST.get('name'),
            hostel_type=request.POST.get('hostel_type'),
            campus=request.POST.get('campus'),
            village=request.POST.get('location'),
            price_per_semester=request.POST.get('price'),
            total_rooms=request.POST.get('total_rooms'),
            description=request.POST.get('description', ''),
            contact_phone=request.POST.get('contact_phone'),
            is_verified=False  # Needs admin approval
        )
        
        messages.success(request, 'Hostel created successfully! It will be reviewed by admin.')
        return redirect('landlord:dashboard')
    
    # Get all facilities for checkboxes
    facilities = Facility.objects.all()
    
    return render(request, 'hostels/create.html', {
        'facilities': facilities
    })