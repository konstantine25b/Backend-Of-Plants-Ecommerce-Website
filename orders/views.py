from rest_framework import generics

from orders.filters import OrderFilter, OrderItemFilter
from users.models import CustomUser
from .models import *
from .serializers import (
   
     OrderSerializer,
    OrderItemSerializer
)
from .permissions import (   CustomOrderItemPermission, CustomOrderPermission)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

    
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
            return super().get_queryset()
        elif self.request.user.is_authenticated:
            # Regular users can only see their own orders
            return Order.objects.filter(customer=self.request.user)
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
    permission_classes = [CustomOrderItemPermission]
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter
    
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
            
    def get_queryset(self):
        if self.request.user.is_staff:
            # Staff members can list all orders
            return super().get_queryset()
        elif self.request.user.is_authenticated:
            # Regular users can only see their own orders
            return OrderItem.objects.filter(customer=self.request.user)
        else:
            return OrderItem.objects.none() 
    

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission]

            
    def update(self, request, *args, **kwargs):
        if self.request.user.role == 'Customer':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=self.request.user)
            return Response(serializer.data)
        elif self.request.user.is_staff:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        