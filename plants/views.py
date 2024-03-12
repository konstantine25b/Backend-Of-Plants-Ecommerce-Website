from rest_framework import generics, permissions
from .models import *
from .serializers import (
    CustomerSerializer, VendorSerializer, AdminSerializer,
    CategorySerializer, ProductSerializer, OrderSerializer,
    OrderItemSerializer, ReviewSerializer
)
from .permissions import IsCustomer, IsVendor, IsAdmin

# Customer views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer | IsAdmin]

# Vendor views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor | IsAdmin]

# Admin views
class AdminListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Admin')
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# Category views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# Product views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor | IsAdmin]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor | IsAdmin]

# Order views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# OrderItem views
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# Review views
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
