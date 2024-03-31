from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category, SubCategory
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
        
  
  
#SubCategory tests

class SubCategoryAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title="Category", description="Category Description")
        self.subcategory1 = SubCategory.objects.create(title="SubCategory 1", category=self.category)
        self.subcategory2 = SubCategory.objects.create(title="SubCategory 2", category=self.category)
        self.staff_user = User.objects.create_superuser(username='staff', email='staff@example.com', password='staffpassword', is_staff=True, role='Admin')
        self.regular_user = User.objects.create_user(username='regular', email='regular@example.com', password='regularpassword')
       
    def test_list_subcategories(self):
        response = self.client.get(reverse('subcategory-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are two subcategories in the database

    def test_retrieve_subcategory(self):
        response = self.client.get(reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.subcategory1.title)
        self.assertEqual(response.data['category'], self.category.pk)  # Assuming response contains category id

    def test_create_subcategory_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        new_subcategory_data = {'title': 'New SubCategory', 'category': self.category.pk}
        response = self.client.post(reverse('subcategory-list-create'), data=new_subcategory_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubCategory.objects.count(), 3)  # Assuming 3 subcategories after creation

    def test_create_subcategory_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        new_subcategory_data = {'title': 'New SubCategory', 'category': self.category.pk}
        response = self.client.post(reverse('subcategory-list-create'), data=new_subcategory_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SubCategory.objects.count(), 2)  # SubCategory count remains the same
        
    def test_update_subcategory_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        updated_subcategory_data = {'title': 'Updated SubCategory', 'category': self.category.pk}
        response = self.client.put(reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk}), data=updated_subcategory_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubCategory.objects.get(pk=self.subcategory1.pk).title, 'Updated SubCategory')

    def test_update_subcategory_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        updated_subcategory_data = {'title': 'Updated SubCategory', 'category': self.category.pk}
        response = self.client.put(reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk}), data=updated_subcategory_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SubCategory.objects.get(pk=self.subcategory1.pk).title, 'SubCategory 1')

    def test_delete_subcategory_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(reverse('subcategory-detail', kwargs={'pk': self.subcategory2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubCategory.objects.filter(pk=self.subcategory2.pk).exists())

    def test_delete_subcategory_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(reverse('subcategory-detail', kwargs={'pk': self.subcategory2.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(SubCategory.objects.filter(pk=self.subcategory2.pk).exists())


      
# Products Tests

class ProductAPITest(TestCase):
    
      
    def setUp(self):
        self.client = APIClient()
        self.vendor_user = User.objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', is_staff=True, role='Admin')
        
        # Create a category
        self.category = Category.objects.create(title="Test Category", description="Category for testing")
        
        # Create subcategories associated with the category
        self.subcategory1 = SubCategory.objects.create(title="SubCategory 1", category=self.category)
        self.subcategory2 = SubCategory.objects.create(title="SubCategory 2", category=self.category)
        
        # Create products associated with the subcategories
        self.product1 = Product.objects.create(vendor=self.vendor_user, subcategory=self.subcategory1, title="Product 1", description="Description 1", price=10.00, quantity=5, image_url="https://example.com/image.jpg")
        self.product2 = Product.objects.create(vendor=self.vendor_user, subcategory=self.subcategory2, title="Product 2", description="Description 2", price=15.00, quantity=10, image_url="https://example.com/image2.jpg")


    

    def test_list_products(self):
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are two products in the database

    def test_retrieve_product(self):
        response = self.client.get(reverse('product-detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Product 1")

    def test_unauthorized_create_product(self):
        data = {'title': 'New Product', 'description': 'New Description', 'price': 20.00, 'quantity': 8, 'image_url': 'https://example.com/new_image.jpg', 'subcategory': self.subcategory1.pk}
        response = self.client.post(reverse('product-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_product(self):
        data = {'title': 'Updated Product', 'description': 'Updated Description', 'price': 25.00, 'quantity': 15, 'image_url': 'https://example.com/updated_image.jpg', 'subcategory': self.subcategory1.pk}
        response = self.client.put(reverse('product-detail', kwargs={'pk': self.product1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_create_product(self):
        # Authenticate as vendor user
        self.client.force_authenticate(user=self.vendor_user)

        data = {'title': 'New Product','vendor': self.vendor_user.pk, 'description': 'New Description', 'price': 20.00, 'quantity': 8, 'image_url': 'https://example.com/new_image.jpg', 'subcategory': self.subcategory1.pk}
        response = self.client.post(reverse('product-list-create'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authorized_update_product(self):
        # Authenticate as admin user
        self.client.force_authenticate(user=self.admin_user)

        data = {'title': 'Updated Product','vendor': self.admin_user.pk, 'description': 'Updated Description', 'price': 25.00, 'quantity': 15, 'image_url': 'https://example.com/updated_image.jpg', 'subcategory': self.subcategory1.pk}
        response = self.client.put(reverse('product-detail', kwargs={'pk': self.product1.pk}), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Product')

    def test_authorized_delete_product(self):
        # Authenticate as admin user
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product1.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_products_by_subcategory(self):
        response = self.client.get(reverse('product-list-create') + f'?subcategory={self.subcategory1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming one product in the subcategory


