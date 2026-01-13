"""
Domain Entity: Book
Clean Architecture - Domain Layer
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal
import uuid


class InsufficientStockError(Exception):
    """Raised when stock is insufficient"""
    pass


@dataclass
class Book:
    """Book Entity - represents a book in the domain"""
    title: str
    author: str
    price: Decimal
    stock: int = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if isinstance(self.price, (int, float)):
            self.price = Decimal(str(self.price))

    def is_in_stock(self) -> bool:
        """Check if book is in stock"""
        return self.stock > 0

    def has_sufficient_stock(self, quantity: int) -> bool:
        """Check if book has sufficient stock"""
        return self.stock >= quantity

    def reduce_stock(self, quantity: int):
        """Reduce stock by quantity"""
        if not self.has_sufficient_stock(quantity):
            raise InsufficientStockError(f"Insufficient stock for {self.title}")
        self.stock -= quantity
        self.updated_at = datetime.utcnow()

    def increase_stock(self, quantity: int):
        """Increase stock by quantity"""
        self.stock += quantity
        self.updated_at = datetime.utcnow()

    def update_price(self, new_price: Decimal):
        """Update book price"""
        self.price = new_price
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': float(self.price),
            'stock': self.stock,
            'is_in_stock': self.is_in_stock(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
