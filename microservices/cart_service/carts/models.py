"""Cart Models for Cart Service (Microservices)"""
import uuid
from django.db import models
from decimal import Decimal


class Cart(models.Model):
    """Cart model - stores cart with customer reference"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=100, unique=True)  # Reference to Customer Service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart for customer {self.customer_id}"

    @property
    def total_price(self):
        """Calculate total price of all items"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Count total items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """CartItem model - stores items with book reference"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.CharField(max_length=100)  # Reference to Book Service
    book_title = models.CharField(max_length=255, default='')  # Cached from Book Service
    book_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))  # Cached from Book Service
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book_id']

    def __str__(self):
        return f"{self.quantity}x {self.book_title}"

    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.book_price * self.quantity
