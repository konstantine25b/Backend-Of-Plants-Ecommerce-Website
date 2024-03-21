from rest_framework import permissions


class CustomUserPermission(permissions.BasePermission):
    """
    Custom permission to allow owners of an object or admins to perform actions.
    """
    def has_permission(self, request, view):
        # Allow GET requests (listing users) for staff members
        # Allow POST requests (creating users) for all users
       
        if request.method == 'GET':
            return request.user and request.user.is_staff
        elif request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow GET, PUT, PATCH, DELETE only if user is the owner or an admin
        if request.method in permissions.SAFE_METHODS:
            return True
       
        return obj == request.user or request.user.is_staff
    
class CustomUserPermission2(permissions.BasePermission):
    """
    Custom permission to allow owners of an object or admins to perform actions.
    """
    

    def has_object_permission(self, request, view, obj):
        # Allow GET, PUT, PATCH, DELETE only if user is the owner or an admin
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

    # def has_permission(self, request, view):
    #     # Allow superadmin to perform any operation
    #     return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Allow staff users to update or delete their own information
        return request.user.is_staff and request.user == obj or request.user.is_superuser
    
    
    
