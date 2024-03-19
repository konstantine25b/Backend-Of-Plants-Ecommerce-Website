from django.urls import path
from . import views

urlpatterns = [
  
    # Order URLs
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),  # List and create orders
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),  # Retrieve, update, delete order
    
    # Order Item URLs
    path('order-items/', views.OrderItemListCreateView.as_view(), name='order-item-list-create'),  # List and create order items
    path('order-items/<int:pk>/', views.OrderItemDetailView.as_view(), name='order-item-detail'),  # Retrieve, update, delete order item
    
]
