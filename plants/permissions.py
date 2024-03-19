# from rest_framework import permissions
# from .models import Product


# class CustomUserPermission(permissions.BasePermission):
#     """
#     Custom permission to allow owners of an object or admins to perform actions.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Allow GET, PUT, PATCH, DELETE only if user is the owner or an admin
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj == request.user or request.user.is_staff
    
# class CustomAdminPermission(permissions.BasePermission):
#     """
#     Custom permission to only allow superusers to create new admin users.
#     """

#     def has_permission(self, request, view):

#         # Check if the user is a superuser
#         return request.user and request.user.is_superuser
    
# class IsSuperAdminOrStaffUpdateDelete(permissions.BasePermission):
#     """
#     Custom permission to allow superadmin to perform any action,
#     and allow staff users to update or delete their own information.
#     """

#     def has_permission(self, request, view):
#         # Allow superadmin to perform any operation
#         return request.user.is_superuser

#     def has_object_permission(self, request, view, obj):
#         # Allow staff users to update or delete their own information
#         return request.user.is_staff and request.user == obj
    
    
# class IsStaffOrSuperuser(permissions.BasePermission):
#     """
#     Custom permission to only allow staff or superuser to access.
#     """

#     def has_permission(self, request, view):
#         return request.user.is_staff or request.user.is_superuser
    

    
    
# class CustomCategoryPermission(permissions.BasePermission):
#     """
#     Custom permission to allow unauthenticated users to view categories,
#     but only authenticated users with admin privileges can modify them.
#     """

#     def has_permission(self, request, view):
#         # Allow GET (list and retrieve) for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Allow modification methods (POST, PUT, PATCH, DELETE) only for authenticated admin users
#         return request.user and request.user.is_authenticated and request.user.is_superuser
    
    
# class IsVendorOrAdminOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow vendors and admins to create products,
#     but allow anyone to read them.
#     """

#     def has_permission(self, request, view):
#         # Allow read-only access to anyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         # Check if the user is authenticated
#         if not request.user.is_authenticated:
#             return False
        
#         # Allow creation only for vendors and admins
#         return request.user.role == 'Vendor' or request.user.is_staff

#     def has_object_permission(self, request, view, obj):
#         # Allow read access to anyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         # Check if the user is authenticated
#         if not request.user.is_authenticated:
#             return False
        
#         # Allow admins to perform any action
#         if request.user.is_staff:
#             return True
        
#         # Ensure that the vendor is the owner of the product
#         return obj.vendor == request.user

# class CustomOrderPermission(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an order and admins to edit it.
#     """
    
#     def has_permission(self, request, view):
#         # Allow only authenticated users to create orders
#         if request.method == 'POST':
#             return request.user.is_authenticated
        
#         # Allow staff and order creators to view their orders
#         if request.method == 'GET':
#             return request.user.is_authenticated and (request.user.is_staff or view.kwargs['user_id'] == str(request.user.id))
        
#         # Allow other methods for authenticated users
#         return True
#     def has_object_permission(self, request, view, obj):
#         # Allow access if the user is an admin
#         if request.user.is_staff:
#             return True
#         # Allow access if the user is the owner of the order
#         return obj.user == request.user
   
   
# class CustomOrderItemPermission1(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an order item and admins
#     to view the list of order items.
#     """

#     def has_permission(self, request, view):
#         # # Allow read-only access to anyone for safe methods
#         # if request.method in permissions.SAFE_METHODS:
#         #     return True
        
#         # Check if the user is authenticated
#         if not request.user.is_authenticated:
#             return False
        
#         # Allow admins to perform any action
#         if request.user.is_staff:
#             return True
        
#          # Allow vendors to perform any action if the product is theirs
#         if request.user.role == 'Vendor':
#             product_id = request.data.get('product')
#             if product_id:
#                 product = Product.objects.filter(pk=product_id, vendor=request.user).exists()
#                 if product:
#                     return True
        
#         # Allow only the owner or admin to create order items
#         return False

#     def has_object_permission(self, request, view, obj):
#         # Allow admins to perform any action
#         if request.user.is_staff:
#             return True
        
#         # Ensure that the user is the owner of the order item
#         return obj.order.user == request.user
# class CustomOrderItemPermission2(permissions.BasePermission):
    
#     """
#     Custom permission to only allow owners of an order item and staff
#     to perform any action on the order item.
#     """

#     def has_permission(self, request, view):
#         # # Allow read-only access to anyone for safe methods
#         # if request.method in permissions.SAFE_METHODS:
#         #     return True
        
#         # Check if the user is authenticated
#         if not request.user.is_authenticated:
#             return False
        
#         # Allow staff members to perform any action
#         if request.user.is_staff:
#             return True
        
#         # Allow vendors to view orders associated with their products
#         if request.user.role == 'Vendor':
#             product_id = request.query_params.get('product')
#             if product_id:
#                 product = Product.objects.filter(pk=product_id, vendor=request.user).exists()
#                 if product:
#                     return True
        
        
#         # Allow only authenticated users to perform actions other than read
#         return False

#     def has_object_permission(self, request, view, obj):
#         # Allow staff members to perform any action
#         if request.user.is_staff:
#             return True
        
#         # Ensure that the user is the owner of the order item
#         return obj.order.user == request.user
# class CustomReviewPermission(permissions.BasePermission):
#     """
#     Custom permission to allow owners of a review and admins to edit or delete it,
#     while allowing everyone to view reviews.
#     """
#     def has_permission(self, request, view):
#         # Allow anyone to view reviews (GET requests)
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Allow authenticated users to create reviews
#         return request.user and request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         # Allow admins to edit or delete any review
#         if request.user and request.user.is_staff:
#             return True
#         # Allow owners of the review to edit or delete it
#         return obj.user == request.user