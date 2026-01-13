"""
Serializers for Clean Architecture
Presentation Layer
"""
from rest_framework import serializers
from datetime import date
from decimal import Decimal


class CustomerInputSerializer(serializers.Serializer):
    """Serializer for customer input"""
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)


class CustomerOutputSerializer(serializers.Serializer):
    """Serializer for customer output"""
    id = serializers.CharField()
    user_name = serializers.CharField()
    phone_number = serializers.CharField(allow_null=True)
    dob = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CustomerUpdateSerializer(serializers.Serializer):
    """Serializer for customer update"""
    phone_number = serializers.CharField(max_length=20, required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)


class BookInputSerializer(serializers.Serializer):
    """Serializer for book input"""
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(default=0, min_value=0)


class BookOutputSerializer(serializers.Serializer):
    """Serializer for book output"""
    id = serializers.CharField()
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    is_in_stock = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class BookUpdateSerializer(serializers.Serializer):
    """Serializer for book update"""
    title = serializers.CharField(max_length=255, required=False)
    author = serializers.CharField(max_length=255, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    stock = serializers.IntegerField(min_value=0, required=False)


class CartItemOutputSerializer(serializers.Serializer):
    """Serializer for cart item output"""
    id = serializers.CharField()
    book_id = serializers.CharField()
    book_title = serializers.CharField()
    book_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()


class CartOutputSerializer(serializers.Serializer):
    """Serializer for cart output"""
    id = serializers.CharField()
    customer_id = serializers.CharField()
    items = CartItemOutputSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_items = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding item to cart"""
    book_id = serializers.CharField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class UpdateQuantitySerializer(serializers.Serializer):
    """Serializer for updating item quantity"""
    quantity = serializers.IntegerField(min_value=1)


class CheckoutResultSerializer(serializers.Serializer):
    """Serializer for checkout result"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
