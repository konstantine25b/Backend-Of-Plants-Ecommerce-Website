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



class CustomUserPermission(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated users to create users,
    but only authenticated users can use other methods.
    """

    def has_permission(self, request, view):
        # Allow POST (creation) for unauthenticated users
        if request.method == 'POST':
            return True

        # Allow other methods only for authenticated users
        return request.user and request.user.is_authenticated
class IsAdminOrSelfOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        
        # Allow GET, HEAD, or OPTIONS requests (read-only permissions).
        if request.method in permissions.SAFE_METHODS:
            return True
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
        if request.user.is_staff:
            return True

        # Check if the user is a vendor and owns the object.
        return obj == request.user and obj.role == 'Vendor'
    
    
class IsSelfAdminOrMainAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the main admin or self admin to modify their details.
    """

    def has_object_permission(self, request, view, obj):
        # Allow admins to modify their own details.
        if request.user.role == 'Admin' and request.user == obj:
            return True
        
        # Allow the main admin to modify any admin's details.
        return request.user.is_superuser
    
class IsMainAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the main admin to view and add new admin.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated.
        if not request.user.is_authenticated:
            return False

        # Allow GET, HEAD, or OPTIONS requests (read-only permissions).
        if request.method in permissions.SAFE_METHODS:
            # Check if the user is the main admin.
            return request.user.is_superuser

        # For POST requests (creating new admin), only allow if user is the main admin.
        return request.user.is_superuser