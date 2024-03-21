from rest_framework import generics, permissions

from .models import *
from .serializers import (
    CustomerSerializer, VendorSerializer, AdminSerializer,

)
from .permissions import ( CustomAdminPermission,
    CustomUserPermission, CustomUserPermission2, IsSuperAdminOrStaffUpdateDelete)


# Customer views

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all().filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [CustomUserPermission]

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all().filter(role='Customer')
    serializer_class = CustomerSerializer
    permission_classes = [CustomUserPermission2]

# Vendor views
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [CustomUserPermission]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Vendor')
    serializer_class = VendorSerializer
    permission_classes = [CustomUserPermission2]

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
    
    def perform_update(self, serializer):
        user = serializer.save()
        if self.request.user.is_superuser:
            user.is_staff = True
            user.save()
