"""
API Views for Clean Architecture
Presentation Layer
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date

from application.use_cases.customer_use_cases import CreateCustomerDTO, UpdateCustomerDTO
from application.use_cases.book_use_cases import CreateBookDTO, UpdateBookDTO
from application.use_cases.cart_use_cases import AddToCartDTO
from domain.entities.book import InsufficientStockError
from infrastructure.container import container
from .serializers import (
    CustomerInputSerializer, CustomerOutputSerializer, CustomerUpdateSerializer,
    BookInputSerializer, BookOutputSerializer, BookUpdateSerializer,
    CartOutputSerializer, AddToCartSerializer, UpdateQuantitySerializer,
    CheckoutResultSerializer
)


# ==================== Customer Views ====================

class CustomerListView(APIView):
    """List all customers or create a new customer"""

    def get(self, request):
        """Get all customers"""
        customers = container.customer_use_cases.get_all_customers()
        data = [c.to_dict() for c in customers]
        return Response(data)

    def post(self, request):
        """Create a new customer"""
        serializer = CustomerInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            dto = CreateCustomerDTO(
                user_name=serializer.validated_data['user_name'],
                password=serializer.validated_data['password'],
                phone_number=serializer.validated_data.get('phone_number'),
                dob=serializer.validated_data.get('dob')
            )
            customer = container.customer_use_cases.create_customer(dto)
            return Response(customer.to_dict(), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    """Get, update, or delete a specific customer"""

    def get(self, request, customer_id):
        """Get customer by ID"""
        customer = container.customer_use_cases.get_customer(customer_id)
        if not customer:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(customer.to_dict())

    def put(self, request, customer_id):
        """Update customer"""
        serializer = CustomerUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = UpdateCustomerDTO(
            phone_number=serializer.validated_data.get('phone_number'),
            dob=serializer.validated_data.get('dob')
        )
        customer = container.customer_use_cases.update_customer(customer_id, dto)
        if not customer:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(customer.to_dict())

    def delete(self, request, customer_id):
        """Delete customer"""
        success = container.customer_use_cases.delete_customer(customer_id)
        if not success:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Book Views ====================

class BookListView(APIView):
    """List all books or create a new book"""

    def get(self, request):
        """Get all books"""
        query = request.query_params.get('q')
        in_stock = request.query_params.get('in_stock')

        if query:
            books = container.book_use_cases.search_books(query)
        elif in_stock:
            books = container.book_use_cases.get_books_in_stock()
        else:
            books = container.book_use_cases.get_all_books()

        data = [b.to_dict() for b in books]
        return Response(data)

    def post(self, request):
        """Create a new book"""
        serializer = BookInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = CreateBookDTO(
            title=serializer.validated_data['title'],
            author=serializer.validated_data['author'],
            price=serializer.validated_data['price'],
            stock=serializer.validated_data.get('stock', 0)
        )
        book = container.book_use_cases.create_book(dto)
        return Response(book.to_dict(), status=status.HTTP_201_CREATED)


class BookDetailView(APIView):
    """Get, update, or delete a specific book"""

    def get(self, request, book_id):
        """Get book by ID"""
        book = container.book_use_cases.get_book(book_id)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(book.to_dict())

    def put(self, request, book_id):
        """Update book"""
        serializer = BookUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dto = UpdateBookDTO(
            title=serializer.validated_data.get('title'),
            author=serializer.validated_data.get('author'),
            price=serializer.validated_data.get('price'),
            stock=serializer.validated_data.get('stock')
        )
        book = container.book_use_cases.update_book(book_id, dto)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(book.to_dict())

    def delete(self, request, book_id):
        """Delete book"""
        success = container.book_use_cases.delete_book(book_id)
        if not success:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Cart Views ====================

class CartView(APIView):
    """Cart operations for a customer"""

    def get(self, request, customer_id):
        """Get customer's cart"""
        cart = container.cart_use_cases.get_or_create_cart(customer_id)
        return Response(cart.to_dict())


class CartAddItemView(APIView):
    """Add item to cart"""

    def post(self, request, customer_id):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            dto = AddToCartDTO(
                book_id=serializer.validated_data['book_id'],
                quantity=serializer.validated_data.get('quantity', 1)
            )
            cart = container.cart_use_cases.add_to_cart(customer_id, dto)
            return Response(cart.to_dict())
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InsufficientStockError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CartRemoveItemView(APIView):
    """Remove item from cart"""

    def delete(self, request, customer_id, book_id):
        """Remove item from cart"""
        cart = container.cart_use_cases.remove_from_cart(customer_id, book_id)
        return Response(cart.to_dict())


class CartUpdateQuantityView(APIView):
    """Update item quantity in cart"""

    def put(self, request, customer_id, book_id):
        """Update item quantity"""
        serializer = UpdateQuantitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = container.cart_use_cases.update_quantity(
                customer_id, 
                book_id, 
                serializer.validated_data['quantity']
            )
            return Response(cart.to_dict())
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InsufficientStockError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CartClearView(APIView):
    """Clear cart"""

    def delete(self, request, customer_id):
        """Clear all items from cart"""
        cart = container.cart_use_cases.clear_cart(customer_id)
        return Response(cart.to_dict())


class CartCheckoutView(APIView):
    """Checkout cart"""

    def post(self, request, customer_id):
        """Checkout cart"""
        result = container.cart_use_cases.checkout(customer_id)
        serializer = CheckoutResultSerializer({
            'success': result.success,
            'message': result.message,
            'total': result.total
        })
        
        if result.success:
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
