from rest_framework import generics
from products.filters import ProductFilter
from users.models import CustomUser
from .models import *
from .serializers import (
    CategorySerializer, ProductSerializer,
)

from .permissions import (  CustomCategoryPermission, 
      IsVendorOrAdminOrReadOnly)
from django.core.cache import cache
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
  

    # Custom logic for creating products
    def perform_create(self, serializer):
        if self.request.user.role == 'Vendor':
            serializer.save(vendor=self.request.user)
        elif self.request.user.is_staff:
            vendor_id = self.request.data.get('vendor')
            if vendor_id:
                vendor = CustomUser.objects.get(id=vendor_id)
                serializer.save(vendor=vendor)
            else:
                serializer.save(vendor=self.request.user)

  
     # Custom logic for listing products
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)      
        data = ProductSerializer(page, many=True).data
        cache_key = "product_list"
        cache_time = 300
        cache.set(cache_key, data, cache_time)
        return self.get_paginated_response(data)
    
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrAdminOrReadOnly]
    
    
    