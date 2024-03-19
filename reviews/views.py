from rest_framework import generics
from .models import *
from .serializers import (
 ReviewSerializer
)
from .permissions import (  
    CustomReviewPermission)

# Review views

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]
