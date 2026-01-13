"""URL configuration for Cart Service"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('carts.urls')),
    path('health/', lambda r: __import__('django.http', fromlist=['JsonResponse']).JsonResponse({'status': 'healthy', 'service': 'cart-service'})),
]
