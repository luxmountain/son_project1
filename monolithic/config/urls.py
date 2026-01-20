"""
URL configuration for Monolithic Architecture
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Web Interface (Frontend)
    path('', include('shop.web_urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('shop.urls')),
]
