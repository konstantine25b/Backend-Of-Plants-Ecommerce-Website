# from django.urls import path
# from . import views

# urlpatterns = [
#     # Customer URLs
#     path('customers/', views.CustomerListCreateView.as_view(), name='customer-create'),  # create customers
#     path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'), # Retrieve, update, delete customer
    
#     # Vendor URLs
#     path('vendors/', views.VendorListCreateView.as_view(), name='vendor-list-create'),  # List and create vendors
#     path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),  # Retrieve, update, delete vendor
    
#     # Admin URLs
#     path('admins/', views.AdminListCreateView.as_view(), name='admin-list-create'),  # List and create admins
#     path('admins/<int:pk>/', views.AdminDetailView.as_view(), name='admin-detail'),  # Retrieve, update, delete admin
    
#     # Category URLs
#     path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),  # List and create categories
#     path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),  # Retrieve category
    
#     # Product URLs
#     path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),  # List products
#     path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),  # Retrieve product
    
#     # Order URLs
#     path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),  # List and create orders
#     path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),  # Retrieve, update, delete order
    
#     # Order Item URLs
#     path('order-items/', views.OrderItemListCreateView.as_view(), name='order-item-list-create'),  # List and create order items
#     path('order-items/<int:pk>/', views.OrderItemDetailView.as_view(), name='order-item-detail'),  # Retrieve, update, delete order item
    
#     # Review URLs
#     path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),  # List and create reviews
#     path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),  # Retrieve, update, delete review
# ]
