from rest_framework import generics
from rest_framework import serializers
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
    
    #es ro vinc qmnis is ikos vendorad
    def perform_create(self, serializer):
      if self.request.user.role == 'Vendor':
        # If the user is a vendor, assign the product to the vendor
        serializer.save(vendor=self.request.user)
      elif self.request.user.is_staff:
        # If the user is staff, check if a vendor ID is provided in the request data
        vendor_id = self.request.data.get('vendor')
        if vendor_id:
             vendor = CustomUser.objects.get(id=vendor_id)
             serializer.save(vendor=vendor)
        else:
            # If no vendor ID is provided, assign the product to the staff user
            serializer.save(vendor=self.request.user)
    
    # es redisistvis
    def list(self, request, *args, **kwargs):
        # Perform filtering
        queryset = self.filter_queryset(self.get_queryset())

        # Define cache key and time
        cache_key = "product_list"
        cache_time =  300  # 5 minutes

        # Attempt to get data from cache
        data = cache.get(cache_key)

        if not data:
            # Serialize queryset
            data = ProductSerializer(queryset, many=True).data

            # Cache the data
            cache.set(cache_key, data, cache_time)

        return Response(data)
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrAdminOrReadOnly]
    
    