from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from datetime import timedelta
from django.utils import timezone





User = get_user_model()


# tests for customers
class CustomerListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.customer = User.objects.create_user(username='customer1', email='customer1@example.com', password='customerpassword', role='Customer')
        self.vendor = User.objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        
    def test_list_customers1(self):
        response = self.client.get(reverse('customer-create'))
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
        
    def test_list_admin_authenticated(self):
        # Authenticate as a superuser or staff user
        self.client.force_authenticate(user=self.superuser)
        
        # Send a GET request to retrieve the list of customers
        response = self.client.get(reverse('customer-create'))

        # Assert that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_customers_authenticated(self):
        # Authenticate as a superuser or staff user
        self.client.force_authenticate(user=self.customer)
        
        # Send a GET request to retrieve the list of customers
        response = self.client.get(reverse('customer-create'))

        # Assert that the response status code is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_list_vendor_authenticated(self):
        # Authenticate as a superuser or staff user
        self.client.force_authenticate(user=self.vendor)
        
        # Send a GET request to retrieve the list of customers
        response = self.client.get(reverse('customer-create'))

        # Assert that the response status code is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
class CustomerCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')

    def test_create_customer(self):
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('customer-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_customer2(self):
        data = {
            'username': 'customer1',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('customer-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_create_customer_creating_same(self):
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('customer-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('customer-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
class CustomerRetrieveTestCase(TestCase):
    
    
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.customer = User.objects.create_user(username='customer1', email='customer1@example.com', password='customerpassword', role='Customer')

    def test_retrieve_customer_unauthenticated(self):
        response = self.client.get(reverse('customer-detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_retrieve_customer_authenticated_superuser(self):
        
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('customer-detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the retrieved data matches the customer's details
        self.assertEqual(response.data['id'], self.customer.id)
        self.assertEqual(response.data['username'], self.customer.username)
       
        
    def test_retrieve_customer_authenticated_regular_user(self):
        regular_user = User.objects.create_user(username='regular_user', email='regular@example.com', password='regularpassword')
        self.client.force_authenticate(user=regular_user)
        response = self.client.get(reverse('customer-detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_retrieve_customer_authenticated_customer_self(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(reverse('customer-detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the retrieved data matches the customer's details
        self.assertEqual(response.data['id'], self.customer.id)
        self.assertEqual(response.data['username'], self.customer.username)
        # Add assertions for other customer details as needed
        
class CustomerUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.customer = User.objects.create_user(username='customer1', email='customer1@example.com', password='customerpassword', role='Customer')

    def test_update_customer_unauthenticated(self):
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('customer-detail', kwargs={'pk': self.customer.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_customer_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('customer-detail', kwargs={'pk': self.customer.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the customer instance from the database to get updated data
        self.customer.refresh_from_db()
        # Assert that the customer's details have been updated
        self.assertEqual(self.customer.first_name, 'Updated First Name')
        self.assertEqual(self.customer.last_name, 'Updated Last Name')
        self.assertEqual(self.customer.phone_number, '1234567890')

    def test_update_customer_authenticated_regular_user(self):
        regular_user = User.objects.create_user(username='regular_user', email='regular@example.com', password='regularpassword')
        self.client.force_authenticate(user=regular_user)
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('customer-detail', kwargs={'pk': self.customer.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_customer_authenticated_customer_self(self):
        self.client.force_authenticate(user=self.customer)
        data = {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'customerpassword',
            'role': 'Customer',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('customer-detail', kwargs={'pk': self.customer.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the customer instance from the database to get updated data
        self.customer.refresh_from_db()
        # Assert that the customer's details have been updated
        self.assertEqual(self.customer.first_name, 'Updated First Name')
        self.assertEqual(self.customer.last_name, 'Updated Last Name')
        self.assertEqual(self.customer.phone_number, '1234567890')
        
# tests for vendors     
class VendorListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.customer = User.objects.create_user(username='customer1', email='customer1@example.com', password='customerpassword', role='Customer')
        self.vendor = User.objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')

    def test_list_vendors_authenticated_vendor(self):
        # Authenticate as a vendor user
        self.client.force_authenticate(user=self.vendor)
        
        # Send a GET request to retrieve the list of vendors
        response = self.client.get(reverse('vendor-list-create'))

        # Assert that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_vendors_authenticated_superuser(self):
        # Authenticate as a superuser
        self.client.force_authenticate(user=self.superuser)
        
        # Send a GET request to retrieve the list of vendors
        response = self.client.get(reverse('vendor-list-create'))

        # Assert that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_vendors_authenticated_customer(self):
        # Authenticate as a customer user
        self.client.force_authenticate(user=self.customer)
        
        # Send a GET request to retrieve the list of vendors
        response = self.client.get(reverse('vendor-list-create'))

        # Assert that the response status code is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
class VendorCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')

    def test_create_vendor(self):
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('vendor-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_vendor_missing_email(self):
        data = {
            'username': 'vendor1',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('vendor-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_vendor_creating_same(self):
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789'
        }
        response = self.client.post(reverse('vendor-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(reverse('vendor-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class VendorRetrieveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.vendor = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='vendorpassword', role='Vendor')

    def test_retrieve_vendor_unauthenticated(self):
        response = self.client.get(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_vendor_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the retrieved data matches the vendor's details
        self.assertEqual(response.data['id'], self.vendor.id)
        self.assertEqual(response.data['username'], self.vendor.username)
        # Add assertions for other vendor details as needed

    def test_retrieve_vendor_authenticated_regular_user(self):
        regular_user = User.objects.create_user(username='regular_user', email='regular@example.com', password='regularpassword')
        self.client.force_authenticate(user=regular_user)
        response = self.client.get(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_vendor_authenticated_vendor_self(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.get(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the retrieved data matches the vendor's details
        self.assertEqual(response.data['id'], self.vendor.id)
        self.assertEqual(response.data['username'], self.vendor.username)
        # Add assertions for other vendor details as needed

class VendorUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.vendor = User.objects.create_user(username='vendor1', email='vendor1@example.com', password='vendorpassword', role='Vendor')

    def test_update_vendor_unauthenticated(self):
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_vendor_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the vendor instance from the database to get updated data
        self.vendor.refresh_from_db()
        # Assert that the vendor's details have been updated
        self.assertEqual(self.vendor.first_name, 'Updated First Name')
        self.assertEqual(self.vendor.last_name, 'Updated Last Name')
        self.assertEqual(self.vendor.phone_number, '1234567890')

    def test_update_vendor_authenticated_regular_user(self):
        regular_user = User.objects.create_user(username='regular_user', email='regular@example.com', password='regularpassword')
        self.client.force_authenticate(user=regular_user)
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vendor_authenticated_vendor_self(self):
        self.client.force_authenticate(user=self.vendor)
        data = {
            'username': 'vendor1',
            'email': 'vendor1@example.com',
            'password': 'vendorpassword',
            'role': 'Vendor',
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('vendor-detail', kwargs={'pk': self.vendor.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the vendor instance from the database to get updated data
        self.vendor.refresh_from_db()
        # Assert that the vendor's details have been updated
        self.assertEqual(self.vendor.first_name, 'Updated First Name')
        self.assertEqual(self.vendor.last_name, 'Updated Last Name')
        self.assertEqual(self.vendor.phone_number, '1234567890')

# tests for admins
class AdminListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.regular_user = User.objects.create_user(username='user1', email='user1@example.com', password='userpassword')

    def test_list_admins_unauthenticated(self):
        response = self.client.get(reverse('admin-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_admins_authenticated_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('admin-list-create'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_admins_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('admin-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AdminCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.regular_user = User.objects.create_user(username='user1', email='user1@example.com', password='userpassword')

    def test_create_admin_unauthenticated(self):
        data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': 'adminpassword',
            'role': 'Admin',
            'is_staff': True,
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('admin-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin_authenticated_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': 'adminpassword',
            'role': 'Admin',
            'is_staff': True,
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('admin-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_admin_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': 'adminpassword',
            'role': 'Admin',
            'is_staff': True,
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('admin-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AdminRetrieveTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.staff_user = User.objects.create_user(username='staff_user', email='staff@example.com', password='staffpassword', is_staff=True)
        self.other_staff_user = User.objects.create_user(username='other_staff_user', email='other_staff@example.com', password='otherstaffpassword', is_staff=True)

    def test_retrieve_admin_unauthenticated(self):
        response = self.client.get(reverse('admin-detail', kwargs={'pk': self.superuser.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_admin_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('admin-detail', kwargs={'pk': self.superuser.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.superuser.id)
        self.assertEqual(response.data['username'], self.superuser.username)

class AdminUpdateTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.staff_user = User.objects.create_user(username='staff_user', email='staff@example.com', password='staffpassword', is_staff=True ,role="Admin", first_name= 'Updated First Name',
            last_name= 'Updated Last Name',
            phone_number= '1234567890')

    def test_update_admin_unauthenticated(self):
        data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': 'newadminpassword',
            'is_staff': True,
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890',
            'role': 'Admin'
        }
        response = self.client.put(reverse('admin-detail', kwargs={'pk': self.superuser.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_admin_authenticated_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': 'newadminpassword',
            'is_staff': True,
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'phone_number': '1234567890'
        }
        response = self.client.put(reverse('admin-detail', kwargs={'pk': self.staff_user.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the admin instance from the database to get updated data
        self.staff_user.refresh_from_db()
        # Assert that the admin's details have been updated
        self.assertEqual(self.staff_user.username, 'newadmin')
        self.assertEqual(self.staff_user.email, 'newadmin@example.com')
        self.assertTrue(self.staff_user.is_staff)

    def test_update_admin_authenticated_staff_self(self):
       self.client.force_authenticate(user=self.staff_user)
       data = {
           'username': 'updatedstaff',
           'email': 'updatedstaff@example.com',
           'password': 'updatedstaffpassword',
           'is_staff': True,
           'first_name': 'Updated First Name',
           'last_name': 'Updated Last Name',
           'phone_number': '9876543210'
       }
       response = self.client.put(reverse('admin-detail', kwargs={'pk': self.staff_user.pk}), data, format='json')
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       # Refresh the staff user instance from the database to get updated data
       self.staff_user.refresh_from_db()
       # Assert that the staff user's details have been updated
       self.assertEqual(self.staff_user.username, 'updatedstaff')
       self.assertEqual(self.staff_user.email, 'updatedstaff@example.com')
       self.assertTrue(self.staff_user.is_staff)
       # Add more assertions for updated fields as needed
   
    def test_update_admin_authenticated_staff_other(self):
        other_staff_user = User.objects.create_user(username='other_staff_user', email='other_staff@example.com', password='otherstaffpassword', is_staff=True, role ="Admin")
        self.client.force_authenticate(user=self.staff_user)
        data = {
            'username': 'updatedotherstaff',
            'email': 'updatedotherstaff@example.com',
            'password': 'updatedotherstaffpassword',
            'is_staff': True,
            'first_name': 'Updated Other First Name',
            'last_name': 'Updated Other Last Name',
            'phone_number': '9876543210'
        }
        response = self.client.put(reverse('admin-detail', kwargs={'pk': other_staff_user.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure that staff user cannot update other staff users' information
        # Assert that the other staff user's details have not been updated
        other_staff_user.refresh_from_db()
        self.assertNotEqual(other_staff_user.username, 'updatedotherstaff')
        self.assertNotEqual(other_staff_user.email, 'updatedotherstaff@example.com')
        self.assertNotEqual(other_staff_user.first_name, 'Updated Other First Name')
        self.assertNotEqual(other_staff_user.last_name, 'Updated Other Last Name')
        self.assertNotEqual(other_staff_user.phone_number, '9876543210')
        # Add more assertions for other fields as needed
        
class JWTAuthTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', role='Admin')
        self.regular_user = User.objects.create_user(username='cust1', email='user1@example.com', password='userpassword')
        self.regular_user = User.objects.create_user(username='vend1', email='user2@example.com', password='userpassword')
      
    def test_jwt_token(self):
        # Attempt to obtain JWT token for regular user
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'cust1', 'password': 'userpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    
   
    
        
    
