"""
Django ORM Models
Clean Architecture - Infrastructure Layer
"""
import uuid
from django.db import models


class CustomerModel(models.Model):
    """Django ORM Model for Customer"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        app_label = 'persistence'

    def __str__(self):
        return self.user_name


class BookModel(models.Model):
    """Django ORM Model for Book"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        app_label = 'persistence'

    def __str__(self):
        return f"{self.title} by {self.author}"


class CartModel(models.Model):
    """Django ORM Model for Cart"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(
        CustomerModel, 
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        app_label = 'persistence'

    def __str__(self):
        return f"Cart of {self.customer.user_name}"


class CartItemModel(models.Model):
    """Django ORM Model for CartItem"""
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        CartModel, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    book = models.ForeignKey(
        BookModel, 
        on_delete=models.CASCADE, 
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book']
        app_label = 'persistence'

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"
