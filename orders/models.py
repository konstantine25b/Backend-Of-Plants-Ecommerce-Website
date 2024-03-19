from django.db import models
from products.models import Product
from users.models import CustomUser



class Order(models.Model):
    user = models.ForeignKey(CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Customer'})
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" Order Id: {str(self.id)} | User: {self.user}"
   
   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank = False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return f"Order Item Id: {str(self.id)} | Order Id :{self.order} | {self.quantity}"

