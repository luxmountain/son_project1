"""
API Gateway Views
Routes requests to appropriate microservices
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .proxy import service_proxy


class HealthCheckView(APIView):
    """Health check for all services"""
    
    def get(self, request):
        health = service_proxy.health_check()
        all_healthy = all(s.get('healthy', False) for s in health.values())
        return Response({
            'gateway': 'healthy',
            'services': health,
            'all_healthy': all_healthy
        })


# ==================== Customer Routes ====================

class CustomerListView(APIView):
    """Proxy for customer list/create"""
    
    def get(self, request):
        result = service_proxy.get('customer', 'customers/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])
    
    def post(self, request):
        result = service_proxy.post('customer', 'customers/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class CustomerDetailView(APIView):
    """Proxy for customer detail/update/delete"""
    
    def get(self, request, customer_id):
        result = service_proxy.get('customer', f'customers/{customer_id}/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result.get('error', 'Not found')}, status=result['status_code'])
    
    def put(self, request, customer_id):
        result = service_proxy.put('customer', f'customers/{customer_id}/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])
    
    def delete(self, request, customer_id):
        result = service_proxy.delete('customer', f'customers/{customer_id}/')
        if result['success']:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': result['error']}, status=result['status_code'])


# ==================== Book Routes ====================

class BookListView(APIView):
    """Proxy for book list/create"""
    
    def get(self, request):
        params = {}
        if request.query_params.get('q'):
            result = service_proxy.get('book', 'books/search/', params={'q': request.query_params['q']})
        elif request.query_params.get('in_stock'):
            result = service_proxy.get('book', 'books/in_stock/')
        else:
            result = service_proxy.get('book', 'books/')
        
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])
    
    def post(self, request):
        result = service_proxy.post('book', 'books/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class BookDetailView(APIView):
    """Proxy for book detail/update/delete"""
    
    def get(self, request, book_id):
        result = service_proxy.get('book', f'books/{book_id}/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result.get('error', 'Not found')}, status=result['status_code'])
    
    def put(self, request, book_id):
        result = service_proxy.put('book', f'books/{book_id}/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])
    
    def delete(self, request, book_id):
        result = service_proxy.delete('book', f'books/{book_id}/')
        if result['success']:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': result['error']}, status=result['status_code'])


# ==================== Cart Routes ====================

class CartView(APIView):
    """Proxy for cart operations"""
    
    def get(self, request, customer_id):
        result = service_proxy.get('cart', f'carts/by-customer/{customer_id}/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class CartAddItemView(APIView):
    """Proxy for adding item to cart"""
    
    def post(self, request, customer_id):
        result = service_proxy.post('cart', f'carts/{customer_id}/add-item/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result.get('error', result.get('data', 'Error'))}, status=result['status_code'])


class CartRemoveItemView(APIView):
    """Proxy for removing item from cart"""
    
    def delete(self, request, customer_id, book_id):
        result = service_proxy.delete('cart', f'carts/{customer_id}/remove-item/{book_id}/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class CartUpdateQuantityView(APIView):
    """Proxy for updating cart item quantity"""
    
    def put(self, request, customer_id, book_id):
        result = service_proxy.put('cart', f'carts/{customer_id}/update-quantity/{book_id}/', data=request.data)
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class CartClearView(APIView):
    """Proxy for clearing cart"""
    
    def delete(self, request, customer_id):
        result = service_proxy.delete('cart', f'carts/{customer_id}/clear/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response({'error': result['error']}, status=result['status_code'])


class CartCheckoutView(APIView):
    """Proxy for cart checkout"""
    
    def post(self, request, customer_id):
        result = service_proxy.post('cart', f'carts/{customer_id}/checkout/')
        if result['success']:
            return Response(result['data'], status=result['status_code'])
        return Response(result.get('data', {'error': result['error']}), status=result['status_code'])
