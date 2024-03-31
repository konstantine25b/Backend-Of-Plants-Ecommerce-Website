
from django.urls import path
from . import views


urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),  # List and create categories
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),  # Retrieve category
    
    # SUbCategory URLS
    path('subcategories/', views.SubCategoryListCreateView.as_view(), name='subcategory-list-create'),  # List and create categories
    path('subcategories/<int:pk>/', views.SubCategoryDetailView.as_view(), name='subcategory-detail'),  # Retrieve category
    
    # Product URLs
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),  # List products
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),  # Retrieve product
]   