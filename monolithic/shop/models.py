"""
Models for Monolithic Architecture
Based on UML Diagram: Customer, Cart, CartItem, Book
"""
import uuid
from django.db import models


class Customer(models.Model):
    """Customer model - stores user information"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return self.user_name


class Book(models.Model):
    """Book model - stores book information"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False


class Cart(models.Model):
    """Cart model - represents a shopping cart for a customer"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart of {self.customer.user_name}"

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Count total items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """CartItem model - represents an item in a cart"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book']

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in {self.cart}"

    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.book.price * self.quantity
