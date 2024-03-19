from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        default=''
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
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='%(class)s_groups'  # Dynamic related name based on the inheriting class
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='%(class)s_permissions'  # Dynamic related name based on the inheriting class
    )
    
    def get_role(self):
        return self.role
    
    def save(self, *args, **kwargs):
        if not self.username:  # Set username to email if it's not provided
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class CustomUser(BaseUser):
    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Vendor', 'Vendor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Customer')

    def __str__(self):
        return f"{self.role} | {self.email}"
        
    def save(self, *args, **kwargs):
        if self.pk is None and self.is_superuser:  # If the user is a superuser and being created
            self.role = 'Admin'  # Set role to 'Admin'
            self.is_staff = True  # Make the user staff
        super().save(*args, **kwargs)

