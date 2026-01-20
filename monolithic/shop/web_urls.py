"""
URL patterns for Web Interface - Monolithic Architecture
"""
from django.urls import path
from . import web_views

urlpatterns = [
    # Home
    path('', web_views.home, name='home'),
    
    # Books
    path('books/', web_views.book_list, name='book_list'),
    path('books/create/', web_views.book_create, name='book_create'),
    path('books/<str:book_id>/', web_views.book_detail, name='book_detail'),
    path('books/<str:book_id>/edit/', web_views.book_edit, name='book_edit'),
    path('books/<str:book_id>/delete/', web_views.book_delete, name='book_delete'),
    
    # Customers
    path('customers/', web_views.customer_list, name='customer_list'),
    path('customers/create/', web_views.customer_create, name='customer_create'),
    path('customers/<str:customer_id>/', web_views.customer_detail, name='customer_detail'),
    path('customers/<str:customer_id>/edit/', web_views.customer_edit, name='customer_edit'),
    path('customers/<str:customer_id>/delete/', web_views.customer_delete, name='customer_delete'),
    path('customers/<str:customer_id>/cart/', web_views.customer_cart, name='customer_cart'),
    
    # Carts
    path('carts/', web_views.cart_list, name='cart_list'),
    path('carts/<str:cart_id>/', web_views.cart_detail, name='cart_detail'),
    path('carts/<str:cart_id>/clear/', web_views.cart_clear, name='cart_clear'),
    path('carts/<str:cart_id>/checkout/', web_views.cart_checkout, name='cart_checkout'),
    path('carts/<str:cart_id>/remove/<str:book_id>/', web_views.cart_remove_item, name='cart_remove_item'),
    
    # Cart actions
    path('add-to-cart/', web_views.add_to_cart, name='add_to_cart'),
    path('cart-item/<str:item_id>/update/', web_views.cart_update_quantity, name='cart_update_quantity'),
]
