"""Service Clients for Cart Service (Microservices)
Handles inter-service communication
"""
import requests
from django.conf import settings


class CustomerServiceClient:
    """Client for Customer Service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'CUSTOMER_SERVICE_URL', 'http://localhost:8001')
    
    def verify_customer(self, customer_id: str) -> dict:
        """Verify customer exists"""
        try:
            response = requests.post(
                f"{self.base_url}/api/customers/{customer_id}/verify/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return {'exists': False}
        except requests.RequestException:
            return {'exists': False, 'error': 'Customer service unavailable'}
    
    def get_customer(self, customer_id: str) -> dict:
        """Get customer details"""
        try:
            response = requests.get(
                f"{self.base_url}/api/customers/{customer_id}/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None


class BookServiceClient:
    """Client for Book Service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8002')
    
    def get_book(self, book_id: str) -> dict:
        """Get book details"""
        try:
            response = requests.get(
                f"{self.base_url}/api/books/{book_id}/",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    def check_stock(self, book_id: str, quantity: int) -> dict:
        """Check if book has sufficient stock"""
        try:
            response = requests.get(
                f"{self.base_url}/api/books/{book_id}/check_stock/",
                params={'quantity': quantity},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return {'has_sufficient_stock': False, 'error': 'Book not found'}
        except requests.RequestException:
            return {'has_sufficient_stock': False, 'error': 'Book service unavailable'}
    
    def bulk_check_stock(self, items: list) -> dict:
        """Bulk check stock for multiple books"""
        try:
            response = requests.post(
                f"{self.base_url}/api/books/bulk_check/",
                json={'items': items},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return {'all_available': False, 'error': 'Failed to check stock'}
        except requests.RequestException:
            return {'all_available': False, 'error': 'Book service unavailable'}
    
    def bulk_reduce_stock(self, items: list) -> dict:
        """Bulk reduce stock for multiple books"""
        try:
            response = requests.post(
                f"{self.base_url}/api/books/bulk_reduce/",
                json={'items': items},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return {'results': [], 'error': 'Failed to reduce stock'}
        except requests.RequestException:
            return {'results': [], 'error': 'Book service unavailable'}


# Singleton instances
customer_client = CustomerServiceClient()
book_client = BookServiceClient()
