from rest_framework import permissions
from .models import CustomUser


class CustomUserPermission(permissions.BasePermission):
    """
    Custom permission to allow owners of an object or admins to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, PUT, PATCH, DELETE only if user is the owner or an admin
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_staff
    
class CustomAdminPermission(permissions.BasePermission):
    """
    Custom permission to only allow superusers to create new admin users.
    """

    def has_permission(self, request, view):

        # Check if the user is a superuser
        return request.user and request.user.is_superuser
    
class IsSuperAdminOrStaffUpdateDelete(permissions.BasePermission):
    """
    Custom permission to allow superadmin to perform any action,
    and allow staff users to update or delete their own information.
    """

    def has_permission(self, request, view):
        # Allow superadmin to perform any operation
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Allow staff users to update or delete their own information
        return request.user.is_staff and request.user == obj
    
    
class IsStaffOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow staff or superuser to access.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser
    

    
    
class CustomCategoryPermission(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated users to view categories,
    but only authenticated users with admin privileges can modify them.
    """

    def has_permission(self, request, view):
        # Allow GET (list and retrieve) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow modification methods (POST, PUT, PATCH, DELETE) only for authenticated admin users
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
    
class IsVendorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow vendors and admins to create products,
    but allow anyone to read them.
    """

    def has_permission(self, request, view):
        # Allow read-only access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow creation only for vendors and admins
        return request.user.role == 'Vendor' or request.user.role == 'Admin'

    def has_object_permission(self, request, view, obj):
        # Allow read access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow admins to perform any action
        if request.user.role == 'Admin':
            return True
        
        # Ensure that the vendor is the owner of the product
        return obj.vendor == request.user

class CustomOrderPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order and admins to edit it.
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users to create orders
        if request.method == 'POST':
            return request.user.is_authenticated
        # Allow other methods for authenticated users
        return True
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        # Allow access if the user is the owner of the order
        return obj.user == request.user
    
class CustomOrderItemPermission(permissions.BasePermission):
    """
    Custom permission to allow owners of an order item, vendors of products
    in the order item, and admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        # Allow access if the user is the owner of the order item
        if obj.order.user == request.user:
            return True
        # Allow access if the user is a vendor of a product in the order item
        if request.user.role == 'Vendor' and obj.product.vendor == request.user:
            return True
        return False
    
class CustomReviewPermission(permissions.BasePermission):
    """
    Custom permission to allow owners of a review and admins to edit or delete it,
    while allowing everyone to view reviews.
    """
    def has_permission(self, request, view):
        # Allow anyone to view reviews (GET requests)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow authenticated users to create reviews
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow admins to edit or delete any review
        if request.user and request.user.is_staff:
            return True
        # Allow owners of the review to edit or delete it
        return obj.user == request.user