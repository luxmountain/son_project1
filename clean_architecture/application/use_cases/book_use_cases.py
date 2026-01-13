"""
Book Use Cases
Clean Architecture - Application Layer
"""
from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal
from domain.entities.book import Book
from domain.repositories.interfaces import BookRepository


@dataclass
class CreateBookDTO:
    """DTO for creating a book"""
    title: str
    author: str
    price: Decimal
    stock: int = 0


@dataclass
class UpdateBookDTO:
    """DTO for updating a book"""
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None


class BookUseCases:
    """Use cases for Book operations"""

    def __init__(self, book_repository: BookRepository):
        self._repository = book_repository

    def create_book(self, dto: CreateBookDTO) -> Book:
        """Create a new book"""
        book = Book(
            title=dto.title,
            author=dto.author,
            price=dto.price,
            stock=dto.stock
        )
        return self._repository.save(book)

    def get_book(self, book_id: str) -> Optional[Book]:
        """Get a book by ID"""
        return self._repository.get_by_id(book_id)

    def get_all_books(self) -> List[Book]:
        """Get all books"""
        return self._repository.get_all()

    def get_books_in_stock(self) -> List[Book]:
        """Get all books that are in stock"""
        return self._repository.get_in_stock()

    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author"""
        return self._repository.search(query)

    def update_book(self, book_id: str, dto: UpdateBookDTO) -> Optional[Book]:
        """Update a book"""
        book = self._repository.get_by_id(book_id)
        if not book:
            return None

        if dto.title:
            book.title = dto.title
        if dto.author:
            book.author = dto.author
        if dto.price is not None:
            book.update_price(dto.price)
        if dto.stock is not None:
            book.stock = dto.stock

        return self._repository.save(book)

    def delete_book(self, book_id: str) -> bool:
        """Delete a book"""
        return self._repository.delete(book_id)

    def update_stock(self, book_id: str, quantity: int) -> Optional[Book]:
        """Update book stock"""
        book = self._repository.get_by_id(book_id)
        if not book:
            return None

        if quantity > 0:
            book.increase_stock(quantity)
        elif quantity < 0:
            book.reduce_stock(abs(quantity))

        return self._repository.save(book)
