from django.contrib import admin
from .models import Hostel, HostelImage, Facility, HostelFacility, Review

class HostelImageInline(admin.TabularInline):
    """Inline admin for hostel images"""
    model = HostelImage
    extra = 3  # Show 3 empty image slots

class HostelFacilityInline(admin.TabularInline):
    """Inline admin for hostel facilities"""
    model = HostelFacility
    extra = 5

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    """Customize hostel admin display"""
    list_display = ('name', 'landlord', 'campus', 'price_per_semester', 'is_verified', 'available_rooms')
    list_filter = ('is_verified', 'hostel_type', 'campus')
    search_fields = ('name', 'landlord__username', 'village')
    inlines = [HostelImageInline, HostelFacilityInline]
    
    actions = ['mark_verified']
    
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} hostels marked as verified")
    mark_verified.short_description = "Mark selected hostels as verified"
    
    def available_rooms(self, obj):
        return obj.available_rooms
    available_rooms.short_description = 'Rooms Available'

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'student', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('hostel__name', 'student__username')