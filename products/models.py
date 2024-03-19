from django.db import models
from django.contrib.auth import get_user_model


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
        get_user_model(),  # Use the custom user model
        on_delete=models.CASCADE,
        # No limit_choices_to parameter, allowing both vendors and admins
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
   
