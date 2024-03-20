from rest_framework import generics

from orders.filters import OrderFilter, OrderItemFilter
from users.models import CustomUser
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
      if self.request.user.role == 'Customer':
        # If the user is a vendor, assign the product to the vendor
        serializer.save(customer=self.request.user)
      elif self.request.user.is_staff:
        # If the user is staff, check if a vendor ID is provided in the request data
        customer_id = self.request.data.get('customer')
        if customer_id:
             customer = CustomUser.objects.get(id=customer_id)
             serializer.save(customer=customer)
        else:
            # If no vendor ID is provided, assign the product to the staff user
            serializer.save(customer=self.request.user)



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomOrderPermission]

# OrderItem views
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission1]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter
    
    def perform_create(self, serializer):
        # Automatically set the user of the order item as the current user
        serializer.save(user=self.request.user)

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission2]
