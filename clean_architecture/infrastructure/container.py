"""
Dependency Injection Container
Clean Architecture - Infrastructure Layer
"""
from application.use_cases.customer_use_cases import CustomerUseCases
from application.use_cases.book_use_cases import BookUseCases
from application.use_cases.cart_use_cases import CartUseCases
from infrastructure.persistence.repositories import (
    DjangoCustomerRepository,
    DjangoBookRepository,
    DjangoCartRepository,
    DjangoCartItemRepository
)


class Container:
    """Simple dependency injection container"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize repositories and use cases"""
        # Repositories
        self._customer_repository = DjangoCustomerRepository()
        self._book_repository = DjangoBookRepository()
        self._cart_repository = DjangoCartRepository()
        self._cart_item_repository = DjangoCartItemRepository()
        
        # Use cases
        self._customer_use_cases = CustomerUseCases(self._customer_repository)
        self._book_use_cases = BookUseCases(self._book_repository)
        self._cart_use_cases = CartUseCases(self._cart_repository, self._book_repository)
    
    @property
    def customer_use_cases(self) -> CustomerUseCases:
        return self._customer_use_cases
    
    @property
    def book_use_cases(self) -> BookUseCases:
        return self._book_use_cases
    
    @property
    def cart_use_cases(self) -> CartUseCases:
        return self._cart_use_cases


# Global container instance
container = Container()
