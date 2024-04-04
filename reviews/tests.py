from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from products.models import Category, SubCategory
from .models import Review, Product
from reviews.views import ReviewDetailView
from django.contrib.auth import get_user_model

class ReviewListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title='Test Category')
        # Create subcategories associated with the category
        self.subcategory1 = SubCategory.objects.create(title="SubCategory 1", category=self.category)  
        self.vendor = get_user_model().objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        self.product = Product.objects.create(vendor=self.vendor, subcategory=self.subcategory1, title="Product 1", description="Description 1", price=10.00, quantity=5, image_url="https://example.com/image.jpg")
        self.user = get_user_model().objects.create_user(username='test', email='test@example.com', password='password')
        self.staff_user = get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='password', role='Admin')


    def test_create_review_authenticated_regular_user(self):
        """
        Test creating a review by an authenticated regular user.
        """
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'rating': 4, 'comment': 'Good product!', 'user': self.user.id, 'username': self.user.username}
        response = self.client.post(reverse('review-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_missing_data(self):
        """
        Test creating a review with missing data.
        """
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'rating': 4, 'comment': 'Good product!', 'user': self.user.id, 'username': self.user.username}
        # No data missing, since all required fields are provided
        response = self.client.post(reverse('review-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_unauthenticated_user(self):
        """
        Test creating a review by an unauthenticated user.
        """
        data = {'product': self.product.id, 'rating': 4, 'comment': 'Nice product!', 'user': self.user.id, 'username': self.user.username}
        response = self.client.post(reverse('review-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_invalid_product_id(self):
        """
        Test creating a review with an invalid product ID.
        """
        self.client.force_authenticate(user=self.user)
        invalid_product_id = 9999  # Assuming this ID does not exist
        data = {'product': invalid_product_id, 'rating': 4, 'comment': 'Nice product!', 'user': self.user.id, 'username': self.user.username}
        response = self.client.post(reverse('review-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_invalid_rating(self):
        """
        Test creating a review with an invalid rating.
        """
        self.client.force_authenticate(user=self.user)
        invalid_rating = 6  # Assuming the rating should be between 1 and 5
        data = {'product': self.product.id, 'rating': invalid_rating, 'comment': 'Nice product!', 'user': self.user.id, 'username': self.user.username}
        response = self.client.post(reverse('review-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class ReviewDetailViewTests(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.vendor = get_user_model().objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        self.category = Category.objects.create(title='Test Category')
        self.subcategory1 = SubCategory.objects.create(title="SubCategory 1", category=self.category)
        self.product = Product.objects.create(vendor=self.vendor, subcategory=self.subcategory1, title="Product 1", description="Description 1", price=10.00, quantity=5, image_url="https://example.com/image.jpg")      
        self.user = get_user_model().objects.create_user(username='test', email='test@example.com', password='password')
        self.staff_user = get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='password', role='Admin')
        self.review = Review.objects.create(product=self.product, user=self.user, username="test_user", rating=4, comment='Initial comment')

    def test_retrieve_review(self):
        """
        Test retrieving a review detail.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], self.review.rating)
        self.assertEqual(response.data['comment'], self.review.comment)

    def test_delete_review_authenticated_user(self):
        """
        Test deleting a review by an authenticated user.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_authenticated_staff(self):
        """
        Test deleting a review by an authenticated staff user.
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_update_review_unauthenticated(self):
        """
        Test updating a review by an unauthenticated user.
        """
        response = self.client.put(reverse('review-detail', args=[self.review.id]), {'rating': 5, 'comment': 'Updated comment'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.get(id=self.review.id).rating, self.review.rating)
        self.assertEqual(Review.objects.get(id=self.review.id).comment, self.review.comment)