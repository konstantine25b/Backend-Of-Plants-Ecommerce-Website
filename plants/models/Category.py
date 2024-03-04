from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100 , required =True)
    description =models.TextField()
    def __str__(self):
        return self.title