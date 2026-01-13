"""Views for Cart Service (Microservices)"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from .models import Cart, CartItem
from .serializers import (
    CartSerializer, CartItemSerializer, AddToCartSerializer,
    UpdateQuantitySerializer, CheckoutResultSerializer
)
from .service_clients import customer_client, book_client


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for Cart - communicates with other services"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def _get_or_create_cart(self, customer_id: str) -> Cart:
        """Get or create cart for customer"""
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        return cart

    @action(detail=False, methods=['get'], url_path='by-customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        """Get cart by customer ID"""
        # Optionally verify customer exists
        # verification = customer_client.verify_customer(customer_id)
        # if not verification.get('exists'):
        #     return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart = self._get_or_create_cart(customer_id)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'], url_path='(?P<customer_id>[^/.]+)/add-item')
    def add_item(self, request, customer_id=None):
        """Add item to cart - calls Book Service for validation"""
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        # Check book exists and has stock via Book Service
        book_data = book_client.get_book(book_id)
        if not book_data:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        stock_check = book_client.check_stock(book_id, quantity)
        if not stock_check.get('has_sufficient_stock'):
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to cart
        cart = self._get_or_create_cart(customer_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={
                'book_title': book_data.get('title', ''),
                'book_price': Decimal(str(book_data.get('price', 0))),
                'quantity': quantity
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['delete'], url_path='(?P<customer_id>[^/.]+)/remove-item/(?P<book_id>[^/.]+)')
    def remove_item(self, request, customer_id=None, book_id=None):
        """Remove item from cart"""
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            CartItem.objects.filter(cart=cart, book_id=book_id).delete()
            return Response(CartSerializer(cart).data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['put'], url_path='(?P<customer_id>[^/.]+)/update-quantity/(?P<book_id>[^/.]+)')
    def update_quantity(self, request, customer_id=None, book_id=None):
        """Update item quantity"""
        serializer = UpdateQuantitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        quantity = serializer.validated_data['quantity']
        
        # Check stock
        stock_check = book_client.check_stock(book_id, quantity)
        if not stock_check.get('has_sufficient_stock'):
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartSerializer(cart).data)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'], url_path='(?P<customer_id>[^/.]+)/clear')
    def clear_cart(self, request, customer_id=None):
        """Clear all items from cart"""
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            cart.items.all().delete()
            return Response(CartSerializer(cart).data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='(?P<customer_id>[^/.]+)/checkout')
    def checkout(self, request, customer_id=None):
        """Checkout cart - orchestrates with Book Service"""
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Cart not found', 'total': 0},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not cart.items.exists():
            return Response(
                {'success': False, 'message': 'Cart is empty', 'total': 0},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare items for bulk operations
        items = [
            {'book_id': item.book_id, 'quantity': item.quantity}
            for item in cart.items.all()
        ]
        
        # Check stock for all items
        stock_check = book_client.bulk_check_stock(items)
        if not stock_check.get('all_available'):
            return Response(
                {'success': False, 'message': 'Some items are out of stock', 'total': 0},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total
        total = cart.total_price
        
        # Reduce stock in Book Service
        reduce_result = book_client.bulk_reduce_stock(items)
        
        # Check if all reductions were successful
        all_success = all(r.get('success', False) for r in reduce_result.get('results', []))
        if not all_success:
            return Response(
                {'success': False, 'message': 'Failed to process checkout', 'total': 0},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return Response({
            'success': True,
            'message': 'Checkout successful',
            'total': float(total)
        })


class CartItemViewSet(viewsets.ModelViewSet):
    """ViewSet for CartItem"""
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
