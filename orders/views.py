from rest_framework import generics

from orders.filters import OrderFilter
from .models import *
from .serializers import (
   
     OrderSerializer,
    OrderItemSerializer
)
from .permissions import (   CustomOrderItemPermission1, CustomOrderItemPermission2, CustomOrderPermission)

from django_filters.rest_framework import DjangoFilterBackend

    
# Order views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomOrderPermission]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    

    def get_queryset(self):
        if self.request.user.is_staff:
            # Staff members can list all orders
            return Order.objects.all()
        elif self.request.user.is_authenticated:
            # Regular users can only see their own orders
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none() 
        

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomOrderPermission]

# OrderItem views
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission1]
    
    def perform_create(self, serializer):
        # Automatically set the user of the order item as the current user
        serializer.save(user=self.request.user)

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission2]
