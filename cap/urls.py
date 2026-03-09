from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('hostels/', include('hostels.urls')),
    path('bookings/', include('bookings.urls')),
    path('landlord/', include('landlord.urls')),
    path('', include('core.urls')),  # ← THIS LINE IS MISSING! ADD IT!
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ), name='password_reset'),
    # ... rest of your password reset URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
path('', include('core.urls')),