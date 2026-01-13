"""Customer Model for Customer Service (Microservices)"""
import uuid
from django.db import models


class Customer(models.Model):
    """Customer model - single responsibility"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.user_name
