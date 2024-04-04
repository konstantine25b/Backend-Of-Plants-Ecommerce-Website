from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from users.models import CustomUser

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=150,
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=False
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Set the username to the username of the user associated with the review
        self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review Id: {self.id} | User: {self.user} | Product: {self.product} | Rating: {self.rating}/5"
    
    
    
