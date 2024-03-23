from rest_framework import permissions
from .models import Order, OrderItem, Product

    
   
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
            return request.user.is_authenticated 
        
        # Allow other methods for authenticated users
        return True
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user.is_staff:
            return True
        
        # Restrict permissions for other users
        if request.method in ['DELETE', 'GET']:
            # Allow DELETE and GET requests if the user is the owner of the order
            return obj.customer == request.user
        
        # For other methods, deny access
        return False
   
   
class CustomOrderItemPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order item and admins
    to view the list of order items.
    """

    def has_permission(self, request, view):
        # Allow read-only access to anyone for safe methods
         # in this method we let staff do anythin , users who have their 
         # order and want to add order items to their order 
       
        if request.method == 'POST'  or request.method=='PUT':
            if not request.user.is_authenticated:
                return False
            if request.user.is_staff:
                return True
           
            
            order_id = request.data.get('order') 
            quantity = request.data.get('quantity') 
            product_id = request.data.get('product') 
            if not order_id:
                return False
            
            
            if not (order_id and product_id and quantity):
                return False
              
            try:
                order = Order.objects.get(id=order_id)
                product = Product.objects.get(id=product_id)
            except (Order.DoesNotExist, Product.DoesNotExist):
                return False
            
            customer_id = request.user.id
            
            if order.customer_id != customer_id:
                return False
             
            if product.quantity < quantity:
                return False
                
            return True
                
        if request.method == 'GET':
             # Allow admins to perform any action
            if request.user.is_staff:
                return True
            customer_id = request.user.id
            queryset = OrderItem.objects.filter(customer_id=customer_id)
            return queryset
            
            
        return False
    
    def has_object_permission(self, request, view, obj):
        # Allow staff members to perform any action
        if request.user.is_staff:
            return True
        
        # Ensure that the user is the owner of the order item
       
        if obj.customer == request.user: 
           
            return True
            
        
        return False
        


