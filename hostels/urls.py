from django.urls import path
from . import views

app_name = 'hostels'

urlpatterns = [
    path('', views.hostel_list, name='list'),
    path('<int:pk>/', views.hostel_detail, name='detail'),
    path('<int:hostel_id>/review/', views.add_review, name='add_review'),
    path('create/', views.hostel_create, name='create'),  # Add this line if missing
]