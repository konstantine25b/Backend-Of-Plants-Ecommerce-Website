from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Customer' , 'Customer'),
        ('Vendor' , 'Vendor'),
        ('Admin' , 'Admin'),
    )
    
    role = models.CharField(max_length = 10 , choices = ROLE_CHOICES, default = 'Customer')
    
    def __str__(self):
        return self.role