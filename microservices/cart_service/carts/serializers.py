"""Serializers for Cart Service (Microservices)"""
from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem"""
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'book_title', 'book_price', 'quantity', 'subtotal', 'created_at']
        read_only_fields = ['id', 'book_title', 'book_price', 'subtotal', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding item to cart"""
    book_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateQuantitySerializer(serializers.Serializer):
    """Serializer for updating quantity"""
    quantity = serializers.IntegerField(min_value=1)


class CheckoutResultSerializer(serializers.Serializer):
    """Serializer for checkout result"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
