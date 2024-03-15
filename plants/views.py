from rest_framework import generics, permissions
from .models import *
from .serializers import (
    CustomerSerializer, VendorSerializer, AdminSerializer,
    CategorySerializer, ProductSerializer, OrderSerializer,
    OrderItemSerializer, ReviewSerializer
)
from .permissions import (CustomCategoryPermission, CustomOrderItemPermission, CustomOrderPermission, CustomProductPermission, IsCustomer, IsVendor, IsAdmin,
    IsUnauthenticatedCustomer , IsAdminOrSelfOrReadOnly, IsVendorOrAdminOrReadOnly,
    IsSelfAdminOrMainAdmin, IsMainAdminOrReadOnly , CustomUserPermission)

# Customer views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomUserPermission]
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrSelfOrReadOnly , permissions.IsAuthenticated]

# Vendor views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [CustomUserPermission]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [IsVendorOrAdminOrReadOnly , permissions.IsAuthenticated]

# Admin views
class AdminListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsMainAdminOrReadOnly]

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfAdminOrMainAdmin]

# Category views
class CategoryListCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomCategoryPermission]

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomCategoryPermission]

# Product views
class ProductListCreateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomProductPermission]

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
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
