from rest_framework import permissions
from .models import Product
    
   
class CustomOrderPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order and admins to edit it.
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users to create orders
        if request.method == 'POST':
            return request.user.is_authenticated
        
        # Allow staff and order creators to view their orders
        if request.method == 'GET':
            return request.user.is_authenticated and (request.user.is_staff or view.kwargs['user_id'] == str(request.user.id))
        
        # Allow other methods for authenticated users
        return True
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user.is_staff:
            return True
        # Allow access if the user is the owner of the order
        return obj.user == request.user
   
   
class CustomOrderItemPermission1(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order item and admins
    to view the list of order items.
    """

    def has_permission(self, request, view):
        # # Allow read-only access to anyone for safe methods
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow admins to perform any action
        if request.user.is_staff:
            return True
        
         # Allow vendors to perform any action if the product is theirs
        if request.user.role == 'Vendor':
            product_id = request.data.get('product')
            if product_id:
                product = Product.objects.filter(pk=product_id, vendor=request.user).exists()
                if product:
                    return True
        
        # Allow only the owner or admin to create order items
        return False

    def has_object_permission(self, request, view, obj):
        # Allow admins to perform any action
        if request.user.is_staff:
            return True
        
        # Ensure that the user is the owner of the order item
        return obj.order.user == request.user
class CustomOrderItemPermission2(permissions.BasePermission):
    
    """
    Custom permission to only allow owners of an order item and staff
    to perform any action on the order item.
    """

    def has_permission(self, request, view):
        # # Allow read-only access to anyone for safe methods
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow staff members to perform any action
        if request.user.is_staff:
            return True
        
        # Allow vendors to view orders associated with their products
        if request.user.role == 'Vendor':
            product_id = request.query_params.get('product')
            if product_id:
                product = Product.objects.filter(pk=product_id, vendor=request.user).exists()
                if product:
                    return True
        
        
        # Allow only authenticated users to perform actions other than read
        return False

    def has_object_permission(self, request, view, obj):
        # Allow staff members to perform any action
        if request.user.is_staff:
            return True
        
        # Ensure that the user is the owner of the order item
        return obj.order.user == request.user
