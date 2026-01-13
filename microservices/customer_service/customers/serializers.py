"""Serializers for Customer Service (Microservices)"""
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""
    
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
