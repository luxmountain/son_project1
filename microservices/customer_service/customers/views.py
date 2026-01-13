"""Views for Customer Service (Microservices)"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, CustomerCreateSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer - Single Responsibility"""
    queryset = Customer.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerSerializer

    @action(detail=False, methods=['get'])
    def by_username(self, request):
        """Get customer by username - for inter-service communication"""
        username = request.query_params.get('username')
        if not username:
            return Response(
                {'error': 'username parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            customer = Customer.objects.get(user_name=username)
            return Response(CustomerSerializer(customer).data)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify customer exists - for inter-service communication"""
        try:
            customer = self.get_object()
            return Response({
                'exists': True,
                'id': customer.id,
                'user_name': customer.user_name
            })
        except:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)
