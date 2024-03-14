from rest_framework import permissions
from .models import CustomUser

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to customers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.Customer


class IsVendor(permissions.BasePermission):
    """
    Allows access only to vendors.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.Vendor


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.Admin

class IsUnauthenticatedCustomer(permissions.BasePermission):
    """
    Allows access to unauthenticated customers.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user == obj:
            return True
        return False
    


class IsVendorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only vendors who own the account or admins to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only permissions).
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an admin.
        if request.user.is_superuser:
            return True

        # Check if the user is a vendor and owns the object.
        return obj == request.user and obj.role == 'Vendor'