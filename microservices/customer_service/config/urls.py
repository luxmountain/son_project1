"""URL configuration for Customer Service"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('customers.urls')),
    path('health/', lambda r: __import__('django.http', fromlist=['JsonResponse']).JsonResponse({'status': 'healthy', 'service': 'customer-service'})),
]
