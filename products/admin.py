from django.contrib import admin
from products.models import Category, Product, SubCategory

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)

