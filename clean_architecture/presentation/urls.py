"""
URL patterns for Clean Architecture
Presentation Layer
"""
from django.urls import path
from .views import (
    CustomerListView, CustomerDetailView,
    BookListView, BookDetailView,
    CartView, CartAddItemView, CartRemoveItemView, 
    CartUpdateQuantityView, CartClearView, CartCheckoutView
)

urlpatterns = [
    # Customer endpoints
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<str:customer_id>/', CustomerDetailView.as_view(), name='customer-detail'),
    
    # Book endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<str:book_id>/', BookDetailView.as_view(), name='book-detail'),
    
    # Cart endpoints
    path('customers/<str:customer_id>/cart/', CartView.as_view(), name='cart'),
    path('customers/<str:customer_id>/cart/items/', CartAddItemView.as_view(), name='cart-add-item'),
    path('customers/<str:customer_id>/cart/items/<str:book_id>/', CartRemoveItemView.as_view(), name='cart-remove-item'),
    path('customers/<str:customer_id>/cart/items/<str:book_id>/quantity/', CartUpdateQuantityView.as_view(), name='cart-update-quantity'),
    path('customers/<str:customer_id>/cart/clear/', CartClearView.as_view(), name='cart-clear'),
    path('customers/<str:customer_id>/cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
]
