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