"""
Domain Entity: Cart
Clean Architecture - Domain Layer
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
import uuid


@dataclass
class CartItem:
    """CartItem Entity - represents an item in a cart"""
    book_id: str
    quantity: int
    book_title: str = ""
    book_price: Decimal = Decimal("0")
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    cart_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if isinstance(self.book_price, (int, float)):
            self.book_price = Decimal(str(self.book_price))

    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal for this item"""
        return self.book_price * self.quantity

    def update_quantity(self, quantity: int):
        """Update item quantity"""
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.quantity = quantity
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book_title,
            'book_price': float(self.book_price),
            'quantity': self.quantity,
            'subtotal': float(self.subtotal),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


@dataclass
class Cart:
    """Cart Entity - represents a shopping cart"""
    customer_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    items: List[CartItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @property
    def total_price(self) -> Decimal:
        """Calculate total price of all items"""
        return sum((item.subtotal for item in self.items), Decimal("0"))

    @property
    def total_items(self) -> int:
        """Count total items in cart"""
        return sum(item.quantity for item in self.items)

    def add_item(self, item: CartItem):
        """Add item to cart"""
        # Check if item already exists
        existing_item = self.find_item_by_book_id(item.book_id)
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.updated_at = datetime.utcnow()
        else:
            item.cart_id = self.id
            self.items.append(item)
        self.updated_at = datetime.utcnow()

    def remove_item(self, book_id: str) -> bool:
        """Remove item from cart"""
        for i, item in enumerate(self.items):
            if item.book_id == book_id:
                self.items.pop(i)
                self.updated_at = datetime.utcnow()
                return True
        return False

    def find_item_by_book_id(self, book_id: str) -> Optional[CartItem]:
        """Find item by book ID"""
        for item in self.items:
            if item.book_id == book_id:
                return item
        return None

    def clear(self):
        """Clear all items from cart"""
        self.items = []
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'items': [item.to_dict() for item in self.items],
            'total_price': float(self.total_price),
            'total_items': self.total_items,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
