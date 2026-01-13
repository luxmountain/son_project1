"""
Repository Interfaces
Clean Architecture - Domain Layer
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.customer import Customer
from domain.entities.book import Book
from domain.entities.cart import Cart, CartItem


class CustomerRepository(ABC):
    """Abstract repository interface for Customer"""

    @abstractmethod
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID"""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Customer]:
        """Get customer by username"""
        pass

    @abstractmethod
    def get_all(self) -> List[Customer]:
        """Get all customers"""
        pass

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """Save customer"""
        pass

    @abstractmethod
    def delete(self, customer_id: str) -> bool:
        """Delete customer"""
        pass


class BookRepository(ABC):
    """Abstract repository interface for Book"""

    @abstractmethod
    def get_by_id(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books"""
        pass

    @abstractmethod
    def get_in_stock(self) -> List[Book]:
        """Get books that are in stock"""
        pass

    @abstractmethod
    def search(self, query: str) -> List[Book]:
        """Search books by title or author"""
        pass

    @abstractmethod
    def save(self, book: Book) -> Book:
        """Save book"""
        pass

    @abstractmethod
    def delete(self, book_id: str) -> bool:
        """Delete book"""
        pass


class CartRepository(ABC):
    """Abstract repository interface for Cart"""

    @abstractmethod
    def get_by_id(self, cart_id: str) -> Optional[Cart]:
        """Get cart by ID"""
        pass

    @abstractmethod
    def get_by_customer_id(self, customer_id: str) -> Optional[Cart]:
        """Get cart by customer ID"""
        pass

    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        """Save cart"""
        pass

    @abstractmethod
    def delete(self, cart_id: str) -> bool:
        """Delete cart"""
        pass


class CartItemRepository(ABC):
    """Abstract repository interface for CartItem"""

    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[CartItem]:
        """Get cart item by ID"""
        pass

    @abstractmethod
    def get_by_cart_id(self, cart_id: str) -> List[CartItem]:
        """Get all items in a cart"""
        pass

    @abstractmethod
    def save(self, item: CartItem) -> CartItem:
        """Save cart item"""
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Delete cart item"""
        pass

    @abstractmethod
    def delete_by_cart_id(self, cart_id: str) -> bool:
        """Delete all items in a cart"""
        pass
