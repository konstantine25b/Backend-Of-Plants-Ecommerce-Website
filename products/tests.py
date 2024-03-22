from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category
from django.contrib.auth import get_user_model
from .models import Product

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

class ProductAPITest(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.vendor_user = User.objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', is_staff=True, role='Admin')
        
        # Create a category
        self.category = Category.objects.create(title="Test Category", description="Category for testing")
        
        # Create products associated with the category
        self.product1 = Product.objects.create(vendor=self.vendor_user, category=self.category, title="Product 1", description="Description 1", price=10.00, quantity=5, image_url="https://example.com/image.jpg")
        self.product2 = Product.objects.create(vendor=self.vendor_user, category=self.category, title="Product 2", description="Description 2", price=15.00, quantity=10, image_url="https://example.com/image2.jpg")


    def test_list_products(self):
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are two products in the database

    def test_retrieve_product(self):
        response = self.client.get(reverse('product-detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Product 1")

    def test_unauthorized_create_product(self):
        data = {'title': 'New Product', 'description': 'New Description', 'price': 20.00, 'quantity': 8, 'image_url': 'https://example.com/new_image.jpg'}
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_product(self):
        data = {'title': 'Updated Product', 'description': 'Updated Description', 'price': 25.00, 'quantity': 15, 'image_url': 'https://example.com/updated_image.jpg'}
        response = self.client.put(reverse('product-detail', kwargs={'pk': self.product1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_vendor_create_product(self):
         # Authenticate as vendor user
         self.client.force_authenticate(user=self.vendor_user)

         # Get the primary key values for an existing category
         category_pk = self.category.pk
         
         data = {'title': 'New Product', 'description': 'New Description', 'price': 20.00, 'quantity': 8, 'image_url': 'https://example.com/new_image.jpg', 'vendor': self.vendor_user.pk, 'category': category_pk}
         response = self.client.post(reverse('product-list-create'), data)
         
         if response.status_code != status.HTTP_201_CREATED:
             print(response.content)
     
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
     # Test authorized update product
    def test_authorized_update_product(self):
        # Authenticate as admin user
        self.client.force_authenticate(user=self.admin_user)
        category_pk = self.category.pk 
        # Update product data
        data = {'title': 'Updated Product', 'description': 'Updated Description', 'price': 25.00, 'quantity': 15, 'image_url': 'https://example.com/updated_image.jpg', 'vendor': self.vendor_user.pk, 'category': category_pk}
        response = self.client.put(reverse('product-detail', kwargs={'pk': self.product1.pk}), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Product')

    # Test authorized delete product
    def test_authorized_delete_product(self):
        # Authenticate as admin user
        self.client.force_authenticate(user=self.admin_user)

        # Delete product
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product1.pk}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
     #Test retrieving products by category
    def test_list_products_by_category(self):
        response = self.client.get(reverse('product-list-create') + f'?category={self.category.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    # Test filtering products by price range
    def test_filter_products_by_price_range(self):
        response = self.client.get(reverse('product-list-create') + '?price__gte=10.00&price__lte=15.00')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)