from rest_framework import generics

from reviews.filters import ReviewFilter
from .models import *
from .serializers import (
 ReviewSerializer
)
from .permissions import (  
    CustomReviewPermission)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Review views

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
    def perform_create(self, serializer):

        
      if self.request.user.is_staff:
        # If the user is staff, check if a vendor ID is provided in the request data
        customer_id = self.request.data.get('user')
        if customer_id:
             customer = CustomUser.objects.get(id=customer_id)
             serializer.save(user=customer)
        else:
            # If no vendor ID is provided, assign the product to the staff user
            serializer.save(user=self.request.user)
            
      else:
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomReviewPermission]
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the serializer
        if self.request.user.is_staff:
            # If the user is staff, check if a user ID is provided in the request data
            user_id = request.data.get('user')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                serializer.save(user=user)
            else:
                # If no user ID is provided, assign the product to the staff user
                serializer.save(user=request.user)
        else:
            serializer.save(user=request.user)
        return Response(serializer.data)
    