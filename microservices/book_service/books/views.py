"""Views for Book Service (Microservices)"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer, StockUpdateSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book - Single Responsibility"""
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
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update book stock - for inter-service communication"""
        book = self.get_object()
        serializer = StockUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            operation = serializer.validated_data['operation']
            
            if operation == 'reduce':
                if book.reduce_stock(quantity):
                    return Response(BookSerializer(book).data)
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                book.increase_stock(quantity)
                return Response(BookSerializer(book).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def check_stock(self, request, pk=None):
        """Check if book has sufficient stock - for inter-service communication"""
        book = self.get_object()
        quantity = int(request.query_params.get('quantity', 1))
        return Response({
            'book_id': book.id,
            'title': book.title,
            'price': str(book.price),
            'stock': book.stock,
            'has_sufficient_stock': book.has_sufficient_stock(quantity)
        })

    @action(detail=False, methods=['post'])
    def bulk_check(self, request):
        """Bulk check stock for multiple books - for checkout"""
        items = request.data.get('items', [])
        results = []
        all_available = True
        
        for item in items:
            book_id = item.get('book_id')
            quantity = item.get('quantity', 1)
            
            try:
                book = Book.objects.get(id=book_id)
                has_stock = book.has_sufficient_stock(quantity)
                if not has_stock:
                    all_available = False
                results.append({
                    'book_id': book_id,
                    'title': book.title,
                    'price': str(book.price),
                    'has_sufficient_stock': has_stock,
                    'available_stock': book.stock
                })
            except Book.DoesNotExist:
                all_available = False
                results.append({
                    'book_id': book_id,
                    'error': 'Book not found'
                })
        
        return Response({
            'all_available': all_available,
            'items': results
        })

    @action(detail=False, methods=['post'])
    def bulk_reduce(self, request):
        """Bulk reduce stock for multiple books - for checkout"""
        items = request.data.get('items', [])
        results = []
        
        for item in items:
            book_id = item.get('book_id')
            quantity = item.get('quantity', 1)
            
            try:
                book = Book.objects.get(id=book_id)
                if book.reduce_stock(quantity):
                    results.append({
                        'book_id': book_id,
                        'success': True,
                        'new_stock': book.stock
                    })
                else:
                    results.append({
                        'book_id': book_id,
                        'success': False,
                        'error': 'Insufficient stock'
                    })
            except Book.DoesNotExist:
                results.append({
                    'book_id': book_id,
                    'success': False,
                    'error': 'Book not found'
                })
        
        return Response({'results': results})
