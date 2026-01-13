"""
Customer Use Cases
Clean Architecture - Application Layer
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import date
from domain.entities.customer import Customer
from domain.repositories.interfaces import CustomerRepository


@dataclass
class CreateCustomerDTO:
    """DTO for creating a customer"""
    user_name: str
    password: str
    phone_number: Optional[str] = None
    dob: Optional[date] = None


@dataclass
class UpdateCustomerDTO:
    """DTO for updating a customer"""
    phone_number: Optional[str] = None
    dob: Optional[date] = None


class CustomerUseCases:
    """Use cases for Customer operations"""

    def __init__(self, customer_repository: CustomerRepository):
        self._repository = customer_repository

    def create_customer(self, dto: CreateCustomerDTO) -> Customer:
        """Create a new customer"""
        # Check if username already exists
        existing = self._repository.get_by_username(dto.user_name)
        if existing:
            raise ValueError(f"Username '{dto.user_name}' already exists")

        customer = Customer(
            user_name=dto.user_name,
            password=dto.password,  # Should be hashed in real app
            phone_number=dto.phone_number,
            dob=dto.dob
        )
        return self._repository.save(customer)

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID"""
        return self._repository.get_by_id(customer_id)

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self._repository.get_all()

    def update_customer(self, customer_id: str, dto: UpdateCustomerDTO) -> Optional[Customer]:
        """Update a customer"""
        customer = self._repository.get_by_id(customer_id)
        if not customer:
            return None

        customer.update_profile(
            phone_number=dto.phone_number,
            dob=dto.dob
        )
        return self._repository.save(customer)

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer"""
        return self._repository.delete(customer_id)

    def authenticate(self, username: str, password: str) -> Optional[Customer]:
        """Authenticate a customer"""
        customer = self._repository.get_by_username(username)
        if customer and customer.password == password:  # Should use proper hashing
            return customer
        return None
