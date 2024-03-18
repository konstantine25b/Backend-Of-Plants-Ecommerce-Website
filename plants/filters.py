import django_filters
from .models import OrderItem, Product, Review


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'vendor__username': ['exact'],  # Filter by vendor username
            'category': ['exact'],    # Filter by category name
            'title': ['icontains'],         # Filter by title (case-insensitive)
            'description': ['icontains'],   # Filter by description (case-insensitive)
            'price': ['exact', 'gte', 'lte'],  # Filter by price (exact, greater than or equal to, less than or equal to)
            'quantity': ['exact', 'gte', 'lte'],  # Filter by quantity (exact, greater than or equal to, less than or equal to)
            'size': ['exact'],              # Filter by size
            'characteristics': ['exact'],   # Filter by characteristics
            'location': ['exact'],          # Filter by location
            'plant_family': ['exact'],      # Filter by plant family
            'water_care': ['exact'],        # Filter by water care
            'is_featured': ['exact'],       # Filter by is_featured
            'is_active': ['exact'],         # Filter by is_active
        }
        
        

class OrderItemFilter(django_filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = {
            'id': ['exact'],
            'order': ['exact'],
            'product': ['exact'],
            'quantity': ['exact', 'gte', 'lte'],
        }
class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            'id': ['exact'],
            'user': ['exact'],
            'product': ['exact'],
            'rating': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
        }