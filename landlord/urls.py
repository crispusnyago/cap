from django.urls import path
from . import views

app_name = 'landlord'

urlpatterns = [
    path('', views.landlord_page, name='index'),
    path('register/', views.landlord_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/<int:hostel_id>/', views.manage_hostel, name='manage_hostel'),
]