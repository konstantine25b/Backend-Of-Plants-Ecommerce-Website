from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model



class Order(models.Model):
    customer = models.ForeignKey(get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders")
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" Order Id: {str(self.id)} | User: {self.customer}"
    
    def total_cost(self):
        """
        Total cost of all the items in an order
        """
        return round(sum([order_item.cost() for order_item in self.order_items.all()]), 2)

   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(blank = False) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  
    
    def __str__(self):
        
        return f"Order Item Id: {str(self.id)} | Order Id :{self.order} | {self.quantity}"
    
    def cost(self):
        """
        Total cost of the ordered item
        """
        return round(self.quantity * self.product.price, 2)

