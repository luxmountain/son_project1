"""
Admin configuration for Monolithic Architecture
"""
from django.contrib import admin
from .models import Customer, Book, Cart, CartItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone_number', 'dob', 'created_at']
    search_fields = ['user_name', 'phone_number']
    list_filter = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock', 'created_at']
    search_fields = ['title', 'author']
    list_filter = ['author', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_items', 'total_price', 'created_at']
    search_fields = ['customer__user_name']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book', 'quantity', 'subtotal', 'created_at']
    search_fields = ['book__title', 'cart__customer__user_name']
    list_filter = ['created_at']
