"""Serializers for Book Service (Microservices)"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book"""
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock', 'is_in_stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockUpdateSerializer(serializers.Serializer):
    """Serializer for updating stock"""
    quantity = serializers.IntegerField()
    operation = serializers.ChoiceField(choices=['reduce', 'increase'], default='reduce')
