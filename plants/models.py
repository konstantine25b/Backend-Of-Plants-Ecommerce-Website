from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    Customer= 'Customer'
    Vendor =  'Vendor'
    Admin= 'Admin'
    ROLE_CHOICES = (
        ('Customer' , 'Customer'),
        ('Vendor' , 'Vendor'),
        ('Admin' , 'Admin'),
    )
    
    role = models.CharField(max_length = 10 , choices = ROLE_CHOICES, default = 'Customer')
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        default=None
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    phone_number = models.CharField(
        max_length=16
    )
    
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )
    
    
    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_users'  # Custom related name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users'  # Custom related name
    )
    
    def get_role(self):
        return self.role
    
    def __str__(self):
        return f"{self.role} | {self.email} "

class Category(models.Model):
    title = models.CharField(max_length=100 , blank=False , unique=True,)
    description =models.TextField()
    def __str__(self):
        return self.title



class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    CHARACTERISTICS_CHOICES = (
        ('Easy', 'Easy'),
        ('Air purifying', 'Air purifying'),
        ('Pet friendly', 'Pet friendly'),
        ('Hanging plant', 'Hanging plant'),
    )

    LOCATION_CHOICES = (
        ('Sun', 'Sun'),
        ('Partial sun', 'Partial sun'),
        ('(Half) shade', '(Half) shade'),
    )

    WATER_CARE_CHOICES = (
        ('Weekly', 'Weekly'),
        ('Bi-weekly', 'Bi-weekly'),
        ('Monthly', 'Monthly'),
    )

    PLANT_FAMILY_CHOICES = (
        ('Ferns', 'Ferns'),
        ('Succulents', 'Succulents'),
        ('Palms', 'Palms'),
        ('Cacti', 'Cacti'),
    )

    vendor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Vendor'},  # Limit choices to users with role 'Vendor'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    image_url = models.URLField()  # Add image URL field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True, null=True)
    characteristics = models.CharField(max_length=50, choices=CHARACTERISTICS_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, blank=True, null=True)
    plant_family = models.CharField(max_length=50, choices=PLANT_FAMILY_CHOICES, blank=True, null=True)
    water_care = models.CharField(max_length=20, choices=WATER_CARE_CHOICES, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Customer'})
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
   
   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank = False) 

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=False
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    