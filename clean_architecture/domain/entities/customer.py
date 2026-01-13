"""
Domain Entity: Customer
Clean Architecture - Domain Layer
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid


@dataclass
class Customer:
    """Customer Entity - represents a customer in the domain"""
    user_name: str
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    phone_number: Optional[str] = None
    dob: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update_profile(self, phone_number: str = None, dob: date = None):
        """Update customer profile"""
        if phone_number:
            self.phone_number = phone_number
        if dob:
            self.dob = dob
        self.updated_at = datetime.utcnow()

    def change_password(self, new_password: str):
        """Change customer password"""
        self.password = new_password
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'phone_number': self.phone_number,
            'dob': self.dob.isoformat() if self.dob else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
