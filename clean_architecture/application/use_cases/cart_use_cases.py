"""
Cart Use Cases
Clean Architecture - Application Layer
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from domain.entities.cart import Cart, CartItem
from domain.entities.book import InsufficientStockError
from domain.repositories.interfaces import CartRepository, BookRepository


@dataclass
class AddToCartDTO:
    """DTO for adding item to cart"""
    book_id: str
    quantity: int = 1


@dataclass
class CheckoutResult:
    """Result of checkout operation"""
    success: bool
    message: str
    total: Decimal = Decimal("0")


class CartUseCases:
    """Use cases for Cart operations"""

    def __init__(self, cart_repository: CartRepository, book_repository: BookRepository):
        self._cart_repository = cart_repository
        self._book_repository = book_repository

    def get_or_create_cart(self, customer_id: str) -> Cart:
        """Get customer's cart or create one if doesn't exist"""
        cart = self._cart_repository.get_by_customer_id(customer_id)
        if not cart:
            cart = Cart(customer_id=customer_id)
            cart = self._cart_repository.save(cart)
        return cart

    def get_cart(self, cart_id: str) -> Optional[Cart]:
        """Get cart by ID"""
        return self._cart_repository.get_by_id(cart_id)

    def add_to_cart(self, customer_id: str, dto: AddToCartDTO) -> Cart:
        """Add item to cart"""
        # Get the book
        book = self._book_repository.get_by_id(dto.book_id)
        if not book:
            raise ValueError("Book not found")

        # Check stock
        if not book.has_sufficient_stock(dto.quantity):
            raise InsufficientStockError(f"Not enough stock for {book.title}")

        # Get or create cart
        cart = self.get_or_create_cart(customer_id)

        # Create cart item
        cart_item = CartItem(
            book_id=book.id,
            book_title=book.title,
            book_price=book.price,
            quantity=dto.quantity
        )

        # Add to cart
        cart.add_item(cart_item)
        return self._cart_repository.save(cart)

    def remove_from_cart(self, customer_id: str, book_id: str) -> Cart:
        """Remove item from cart"""
        cart = self.get_or_create_cart(customer_id)
        cart.remove_item(book_id)
        return self._cart_repository.save(cart)

    def update_quantity(self, customer_id: str, book_id: str, quantity: int) -> Cart:
        """Update item quantity in cart"""
        cart = self.get_or_create_cart(customer_id)
        item = cart.find_item_by_book_id(book_id)
        
        if not item:
            raise ValueError("Item not found in cart")

        # Check stock
        book = self._book_repository.get_by_id(book_id)
        if not book.has_sufficient_stock(quantity):
            raise InsufficientStockError(f"Not enough stock for {book.title}")

        item.update_quantity(quantity)
        return self._cart_repository.save(cart)

    def clear_cart(self, customer_id: str) -> Cart:
        """Clear all items from cart"""
        cart = self.get_or_create_cart(customer_id)
        cart.clear()
        return self._cart_repository.save(cart)

    def checkout(self, customer_id: str) -> CheckoutResult:
        """Checkout cart"""
        cart = self._cart_repository.get_by_customer_id(customer_id)
        
        if not cart or not cart.items:
            return CheckoutResult(
                success=False,
                message="Cart is empty"
            )

        # Verify all items have sufficient stock
        for item in cart.items:
            book = self._book_repository.get_by_id(item.book_id)
            if not book:
                return CheckoutResult(
                    success=False,
                    message=f"Book not found: {item.book_title}"
                )
            if not book.has_sufficient_stock(item.quantity):
                return CheckoutResult(
                    success=False,
                    message=f"Not enough stock for {book.title}"
                )

        # Calculate total and reduce stock
        total = cart.total_price
        for item in cart.items:
            book = self._book_repository.get_by_id(item.book_id)
            book.reduce_stock(item.quantity)
            self._book_repository.save(book)

        # Clear cart
        cart.clear()
        self._cart_repository.save(cart)

        return CheckoutResult(
            success=True,
            message="Checkout successful",
            total=total
        )
