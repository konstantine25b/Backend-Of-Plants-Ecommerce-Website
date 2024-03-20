import django_filters
from .models import OrderItem , Order


    
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'id': ['exact'],
            'customer': ['exact'],
            # 'total_cost': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user
        if user.is_anonymous:
            del self.filters['user']    

class OrderItemFilter(django_filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = {
            'id': ['exact'],
            'order': ['exact'],
            'product': ['exact'],
            'quantity': ['exact', 'gte', 'lte'],
        }