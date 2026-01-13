"""Book Model for Book Service (Microservices)"""
import uuid
from django.db import models


class Book(models.Model):
    """Book model - single responsibility"""
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

    def has_sufficient_stock(self, quantity):
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        if self.has_sufficient_stock(quantity):
            self.stock -= quantity
            self.save()
            return True
        return False

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()
