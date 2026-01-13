"""
Repository Implementations
Clean Architecture - Infrastructure Layer
"""
from typing import List, Optional
from django.db.models import Q

from domain.entities.customer import Customer
from domain.entities.book import Book
from domain.entities.cart import Cart, CartItem
from domain.repositories.interfaces import (
    CustomerRepository, BookRepository, CartRepository, CartItemRepository
)
from .models import CustomerModel, BookModel, CartModel, CartItemModel


class DjangoCustomerRepository(CustomerRepository):
    """Django ORM implementation of CustomerRepository"""

    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert ORM model to domain entity"""
        return Customer(
            id=model.id,
            user_name=model.user_name,
            password=model.password,
            phone_number=model.phone_number,
            dob=model.dob,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Customer) -> CustomerModel:
        """Convert domain entity to ORM model"""
        return CustomerModel(
            id=entity.id,
            user_name=entity.user_name,
            password=entity.password,
            phone_number=entity.phone_number,
            dob=entity.dob
        )

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(user_name=username)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def get_all(self) -> List[Customer]:
        models = CustomerModel.objects.all()
        return [self._to_entity(m) for m in models]

    def save(self, customer: Customer) -> Customer:
        CustomerModel.objects.update_or_create(
            id=customer.id,
            defaults={
                'user_name': customer.user_name,
                'password': customer.password,
                'phone_number': customer.phone_number,
                'dob': customer.dob
            }
        )
        return customer

    def delete(self, customer_id: str) -> bool:
        try:
            CustomerModel.objects.get(id=customer_id).delete()
            return True
        except CustomerModel.DoesNotExist:
            return False


class DjangoBookRepository(BookRepository):
    """Django ORM implementation of BookRepository"""

    def _to_entity(self, model: BookModel) -> Book:
        """Convert ORM model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=model.price,
            stock=model.stock,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_by_id(self, book_id: str) -> Optional[Book]:
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None

    def get_all(self) -> List[Book]:
        models = BookModel.objects.all()
        return [self._to_entity(m) for m in models]

    def get_in_stock(self) -> List[Book]:
        models = BookModel.objects.filter(stock__gt=0)
        return [self._to_entity(m) for m in models]

    def search(self, query: str) -> List[Book]:
        models = BookModel.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        return [self._to_entity(m) for m in models]

    def save(self, book: Book) -> Book:
        BookModel.objects.update_or_create(
            id=book.id,
            defaults={
                'title': book.title,
                'author': book.author,
                'price': book.price,
                'stock': book.stock
            }
        )
        return book

    def delete(self, book_id: str) -> bool:
        try:
            BookModel.objects.get(id=book_id).delete()
            return True
        except BookModel.DoesNotExist:
            return False


class DjangoCartRepository(CartRepository):
    """Django ORM implementation of CartRepository"""

    def _to_entity(self, model: CartModel) -> Cart:
        """Convert ORM model to domain entity"""
        items = []
        for item_model in model.items.all():
            items.append(CartItem(
                id=item_model.id,
                cart_id=model.id,
                book_id=item_model.book.id,
                book_title=item_model.book.title,
                book_price=item_model.book.price,
                quantity=item_model.quantity,
                created_at=item_model.created_at,
                updated_at=item_model.updated_at
            ))
        
        return Cart(
            id=model.id,
            customer_id=model.customer.id,
            items=items,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_by_id(self, cart_id: str) -> Optional[Cart]:
        try:
            model = CartModel.objects.prefetch_related('items__book').get(id=cart_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None

    def get_by_customer_id(self, customer_id: str) -> Optional[Cart]:
        try:
            model = CartModel.objects.prefetch_related('items__book').get(customer_id=customer_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None

    def save(self, cart: Cart) -> Cart:
        # Get or create cart model
        cart_model, _ = CartModel.objects.update_or_create(
            id=cart.id,
            defaults={'customer_id': cart.customer_id}
        )

        # Sync items
        existing_item_ids = set(cart_model.items.values_list('book_id', flat=True))
        new_item_book_ids = {item.book_id for item in cart.items}

        # Delete removed items
        cart_model.items.exclude(book_id__in=new_item_book_ids).delete()

        # Update or create items
        for item in cart.items:
            CartItemModel.objects.update_or_create(
                cart=cart_model,
                book_id=item.book_id,
                defaults={'quantity': item.quantity}
            )

        return cart

    def delete(self, cart_id: str) -> bool:
        try:
            CartModel.objects.get(id=cart_id).delete()
            return True
        except CartModel.DoesNotExist:
            return False


class DjangoCartItemRepository(CartItemRepository):
    """Django ORM implementation of CartItemRepository"""

    def _to_entity(self, model: CartItemModel) -> CartItem:
        return CartItem(
            id=model.id,
            cart_id=model.cart.id,
            book_id=model.book.id,
            book_title=model.book.title,
            book_price=model.book.price,
            quantity=model.quantity,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def get_by_id(self, item_id: str) -> Optional[CartItem]:
        try:
            model = CartItemModel.objects.select_related('book').get(id=item_id)
            return self._to_entity(model)
        except CartItemModel.DoesNotExist:
            return None

    def get_by_cart_id(self, cart_id: str) -> List[CartItem]:
        models = CartItemModel.objects.select_related('book').filter(cart_id=cart_id)
        return [self._to_entity(m) for m in models]

    def save(self, item: CartItem) -> CartItem:
        CartItemModel.objects.update_or_create(
            id=item.id,
            defaults={
                'cart_id': item.cart_id,
                'book_id': item.book_id,
                'quantity': item.quantity
            }
        )
        return item

    def delete(self, item_id: str) -> bool:
        try:
            CartItemModel.objects.get(id=item_id).delete()
            return True
        except CartItemModel.DoesNotExist:
            return False

    def delete_by_cart_id(self, cart_id: str) -> bool:
        CartItemModel.objects.filter(cart_id=cart_id).delete()
        return True
