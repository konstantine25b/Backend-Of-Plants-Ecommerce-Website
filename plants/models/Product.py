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
        limit_choices_to={'role': 'Vendor'}  # Limit choices to users with role 'Vendor'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image_url = models.URLField() # ess dummy temaa
    created_at = models.DateTimeField(auto_now_add=True)

    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True, null=True)
    characteristics = models.CharField(max_length=50, choices=CHARACTERISTICS_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, blank=True, null=True)
    plant_family = models.CharField(max_length=50, choices=PLANT_FAMILY_CHOICES, blank=True, null=True)
    water_care = models.CharField(max_length=20, choices=WATER_CARE_CHOICES, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name