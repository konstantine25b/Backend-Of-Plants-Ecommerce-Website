from django.urls import path
from . import views

urlpatterns = [
  
    # Review URLs
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),  # List and create reviews
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),  # Retrieve, update, delete review
]
