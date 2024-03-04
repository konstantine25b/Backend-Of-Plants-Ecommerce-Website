from django.db import models
from .Product import Product
from .Order import Order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,required =True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,required =True)
    quantity = models.IntegerField(required =True)