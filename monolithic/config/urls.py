"""
URL configuration for Monolithic Architecture
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API Root - Welcome page"""
    return JsonResponse({
        'message': 'Welcome to Bookshop API (Monolithic Architecture)',
        'endpoints': {
            'customers': '/api/customers/',
            'books': '/api/books/',
            'carts': '/api/carts/',
            'cart_items': '/api/cart-items/',
            'admin': '/admin/',
        },
        'version': '1.0.0'
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
]
