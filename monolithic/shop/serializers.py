"""
Serializers for Monolithic Architecture
"""
from rest_framework import serializers
from .models import Customer, Book, Cart, CartItem


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    
    class Meta:
        model = Customer
        fields = ['id', 'user_name', 'phone_number', 'dob', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Customer"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Customer
        fields = ['id', 'user_name', 'password', 'phone_number', 'dob']
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock', 'is_in_stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    book = BookSerializer(read_only=True)
    book_id = serializers.CharField(write_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'subtotal', 'created_at']
        read_only_fields = ['id', 'subtotal', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()
    customer_name = serializers.CharField(source='customer.user_name', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'customer_name', 'items', 'total_price', 'total_items', 'created_at']
        read_only_fields = ['id', 'created_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding item to cart"""
    book_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_book_id(self, value):
        try:
            Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value
