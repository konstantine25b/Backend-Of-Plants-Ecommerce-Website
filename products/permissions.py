from rest_framework import permissions
    
    
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
        return request.user.role == 'Vendor' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow read access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow admins to perform any action
        if request.user.is_staff:
            return True
        
        # Ensure that the vendor is the owner of the product
        return obj.vendor == request.user
