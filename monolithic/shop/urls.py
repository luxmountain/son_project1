"""
URL patterns for Monolithic Architecture
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, BookViewSet, CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'books', BookViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
