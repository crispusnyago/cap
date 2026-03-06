from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),  # This connects to your homepage
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]