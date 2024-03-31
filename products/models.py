from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Product(models.Model):
    
    SIZE_CHOICES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
)

    vendor = models.ForeignKey(
        get_user_model(),  # Use the custom user model
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    image_url = models.URLField()  # Add image URL field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
