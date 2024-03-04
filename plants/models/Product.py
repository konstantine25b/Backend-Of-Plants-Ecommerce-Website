from django.db import models
from .Category import Category
from .CustomUser import CustomUser  

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
        limit_choices_to={'role': 'Vendor'},required =True  # Limit choices to users with role 'Vendor'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,required =True)
    title = models.CharField(max_length=255,required =True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2 ,required =True)
    quantity = models.IntegerField(default=0,required =True)
    image_url = models.URLField() # ess dummy temaa
    created_at = models.DateTimeField(auto_now_add=True,required =True)
    updated_at = models.DateTimeField(auto_now=True,required =True)

    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True, required =True)
    characteristics = models.CharField(max_length=50, choices=CHARACTERISTICS_CHOICES, blank=True, required =True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, blank=True, required =True)
    plant_family = models.CharField(max_length=50, choices=PLANT_FAMILY_CHOICES, blank=True, required =True)
    water_care = models.CharField(max_length=20, choices=WATER_CARE_CHOICES, blank=True,required =True)
    is_featured = models.BooleanField(default=False,required =True)
    is_active = models.BooleanField(default=True,required =True)

    def __str__(self):
        return self.name