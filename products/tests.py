from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


# Category Tests
class CategoryAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(title="Category 1", description="Description 1")
        self.category2 = Category.objects.create(title="Category 2", description="Description 2")
        self.staff_user = User.objects.create_superuser(username='staff', email='staff@example.com', password='staffpassword', is_staff=True ,role='Admin')
        self.regular_user = User.objects.create_user(username='regular', email='regular@example.com', password='regularpassword')
       
    def test_list_categories(self):
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are two categories in the database

    def test_retrieve_category(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': self.category1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.category1.title)
        self.assertEqual(response.data['description'], self.category1.description)


    def test_create_category(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {'title': 'New Category', 'description': 'New Description'}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming the new category is added at the end of the paginated list
        response2 = self.client.get(reverse('category-list-create'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), 3) 
        
    def test_update_category(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {'title': 'Updated Category', 'description': 'Updated Description'}
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.title, 'Updated Category')
        self.assertEqual(self.category1.description, 'Updated Description')
        
    def test_delete_category(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assuming the deleted category is removed from the paginated list
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_non_existing_category(self):
        response = self.client.get(reverse('category-detail', kwargs={'pk': 1000}))  # Assuming no category with ID 1000 exists
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_create_category(self):
        data = {'title': 'New Category', 'description': 'New Description'}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_unauthorized_update_category(self):
        data = {'title': 'Updated Category', 'description': 'Updated Description'}
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_category(self):
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_staff_create_category(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {'title': 'New Category', 'description': 'New Description'}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_update_category(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {'title': 'Updated Category', 'description': 'Updated Description'}
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_staff_delete_category(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_create_category(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'title': 'New Category', 'description': 'New Description'}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_update_category(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'title': 'Updated Category', 'description': 'Updated Description'}
        response = self.client.put(reverse('category-detail', kwargs={'pk': self.category1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_delete_category(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(reverse('category-detail', kwargs={'pk': self.category1.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
# Products Tests