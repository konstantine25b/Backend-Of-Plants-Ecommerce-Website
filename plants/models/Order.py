from django.db import models
from .CustomUser import CustomUser 

class Order(models.Model):
    user = models.ForeignKey(CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Customer'} )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)