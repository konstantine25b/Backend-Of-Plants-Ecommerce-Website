from django.urls import path
from . import views


urlpatterns = [
    
  
    
    # Customer URLs
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-create'),  # create customers
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'), # Retrieve, update, delete customer
    
    # Vendor URLs
    path('vendors/', views.VendorListCreateView.as_view(), name='vendor-list-create'),  # List and create vendors
    path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor-detail'),  # Retrieve, update, delete vendor
    
    # Admin URLs
    path('admins/', views.AdminListCreateView.as_view(), name='admin-list-create'),  # List and create admins
    path('admins/<int:pk>/', views.AdminDetailView.as_view(), name='admin-detail'),  # Retrieve, update, delete admin
]