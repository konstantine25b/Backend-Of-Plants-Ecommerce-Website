from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to customers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == 'Customer'


class IsVendor(permissions.BasePermission):
    """
    Allows access only to vendors.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == 'Vendor'


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'

class IsUnauthenticatedCustomer(permissions.BasePermission):
    """
    Allows access to unauthenticated customers.
    """
    def has_permission(self, request, view):
        return request.user.is_anonymous and request.user.role == 'Customer'