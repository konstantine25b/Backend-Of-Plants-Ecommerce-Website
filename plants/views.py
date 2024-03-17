from rest_framework import generics, permissions

from plants.filters import ProductFilter
from .models import *
from .serializers import (
    CustomerSerializer, VendorSerializer, AdminSerializer,
    CategorySerializer, ProductSerializer, OrderSerializer,
    OrderItemSerializer, ReviewSerializer
)
from .permissions import (CustomAdminPermission, CustomCategoryPermission, CustomOrderItemPermission, CustomOrderPermission, CustomProductPermission, 
    CustomReviewPermission, CustomUserPermission, IsSuperAdminOrStaffUpdateDelete, IsVendorOrAdminOrReadOnly)
from django.core.cache import cache
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Customer views

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all().filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all().filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [CustomUserPermission]

# Vendor views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [CustomUserPermission]

# Admin views
class AdminListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        if self.request.user.is_superuser:
            user.role = 'Admin'
            user.is_staff = True
            user.save()
    permission_classes = [CustomAdminPermission]

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    permission_classes = [IsSuperAdminOrStaffUpdateDelete]

# Category views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomCategoryPermission]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomCategoryPermission]

# Product views
# # The `ProductListCreateView` class in Python defines a view for listing and creating products with
# caching implemented for the product list.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrAdminOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter
    
    # def list(self, request, *args, **kwargs):
    #     # Perform filtering
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Define cache key and time
    #     cache_key = "product_list"
    #     cache_time =  300  # 5 minutes

    #     # Attempt to get data from cache
    #     data = cache.get(cache_key)

    #     if not data:
    #         # Serialize queryset
    #         data = ProductSerializer(queryset, many=True).data

    #         # Cache the data
    #         cache.set(cache_key, data, cache_time)

    #     return Response(data)
    
   
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    
# Order views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomOrderPermission]

# OrderItem views
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomOrderItemPermission]

# Review views

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]
