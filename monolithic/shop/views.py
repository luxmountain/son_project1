"""
Views for Monolithic Architecture
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Customer, Book, Cart, CartItem
from .serializers import (
    CustomerSerializer, CustomerCreateSerializer, BookSerializer,
    CartSerializer, CartItemSerializer, AddToCartSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer CRUD operations"""
    queryset = Customer.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerSerializer

    @action(detail=True, methods=['get'])
    def cart(self, request, pk=None):
        """Get customer's cart"""
        customer = self.get_object()
        cart, created = Cart.objects.get_or_create(customer=customer)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book CRUD operations"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """Get all books that are in stock"""
        books = Book.objects.filter(stock__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search books by title or author"""
        query = request.query_params.get('q', '')
        books = Book.objects.filter(
            models.Q(title__icontains=query) | models.Q(author__icontains=query)
        )
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for Cart operations"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add item to cart"""
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        
        if serializer.is_valid():
            book = get_object_or_404(Book, id=serializer.validated_data['book_id'])
            quantity = serializer.validated_data['quantity']
            
            # Check stock
            if book.stock < quantity:
                return Response(
                    {'error': 'Not enough stock available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                book=book,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(CartSerializer(cart).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove item from cart"""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        
        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            cart_item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear all items from cart"""
        cart = self.get_object()
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """Checkout cart - reduce stock and clear cart"""
        cart = self.get_object()
        
        # Check all items have sufficient stock
        for item in cart.items.all():
            if item.book.stock < item.quantity:
                return Response(
                    {'error': f'Not enough stock for {item.book.title}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Reduce stock for all items
        total = 0
        for item in cart.items.all():
            item.book.reduce_stock(item.quantity)
            total += item.subtotal
        
        # Clear cart
        cart.items.all().delete()
        
        return Response({
            'message': 'Checkout successful',
            'total': total
        })


class CartItemViewSet(viewsets.ModelViewSet):
    """ViewSet for CartItem operations"""
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        """Update item quantity"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if quantity < 1:
            return Response(
                {'error': 'Quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if cart_item.book.stock < quantity:
            return Response(
                {'error': 'Not enough stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
