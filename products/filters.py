import django_filters

from products.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'id': ['exact'],
            'vendor': ['exact'],  # Filter by vendor username
            'category': ['exact'],    # Filter by category name
            'title': ['exact'],         # Filter by title (case-insensitive)
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
        