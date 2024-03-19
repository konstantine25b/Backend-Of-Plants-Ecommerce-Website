import django_filters
from .models import Review 

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