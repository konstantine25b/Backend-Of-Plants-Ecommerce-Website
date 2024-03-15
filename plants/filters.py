import django_filters
from .models import OrderItem, Product, Review


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields =['id','vendor', 'category', 'price', 'quantity' ,'title' , 'created_at' , 'size' , 
                 'characteristics', 'location' , 'plant_family' , 'water_care' , 'is_featured' , 'is_active']
        
class OrderItemFilter(django_filters.FilterSet):
    class Meta:
        model =OrderItem
        fields = ['id' , 'order' , 'product' , 'quantity']
        
        
class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model =Review
        fields = ['id' , 'user' , 'product' , 'rating' , 'created_at']
        
    