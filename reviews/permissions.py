from rest_framework import permissions


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