from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem, Product
from products.models import Category
from decimal import Decimal
from orders.views import CustomOrderPermission
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
class OrderModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.customer = get_user_model().objects.create_user(username='testuser', password='password123')
        
        cls.category = Category.objects.create(title='Test Category')
        cls.vendor = get_user_model().objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
    
        # Create a product with the specified vendor
        cls.product = Product.objects.create(
            title='Test Product',
            price=10,
            quantity=5,
            category=cls.category,
            vendor=cls.vendor  # Assign the vendor to the product
        )
        cls.order = Order.objects.create(customer=cls.customer)
    
        
        # Create an order
        cls.order_item1 = OrderItem.objects.create(order=cls.order, product=cls.product, quantity=2, customer=cls.customer)

      
    def test_total_cost(self):
        # Calculate expected total cost based on the quantities and prices of items in the order
        expected_total_cost = Decimal('0')
        for order_item in self.order.order_items.all():
            expected_total_cost += order_item.quantity * order_item.product.price
        
        # Assert that the calculated total cost matches the expected total cost
        self.assertEqual(self.order.total_cost(), expected_total_cost)
        
class OrderItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the order item
         # Create a user for the order item
        cls.customer = get_user_model().objects.create_user(username='testuser', password='password')    
    
        cls.category = Category.objects.create(title='Test Category')
        cls.vendor = get_user_model().objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
    
        # Create a product with the specified vendor
        cls.product = Product.objects.create(
            title='Test Product',
            price=10,
            quantity=5,
            category=cls.category,
            vendor=cls.vendor  # Assign the vendor to the product
        )
        cls.order = Order.objects.create(customer=cls.customer)
    
        # Create an order item with the specified customer
        cls.order_item = OrderItem.objects.create(order=cls.order, product=cls.product, quantity=2, customer=cls.customer)
    
    def test_cost(self):
        # Calculate the expected cost based on the quantity and price of the product
        expected_cost = self.order_item.quantity * self.product.price

        # Verify that the calculated cost matches the expected cost
        self.assertEqual(self.order_item.cost(), expected_cost)
        
    def test_str_representation(self):
        expected_str = f"Order Item Id: {self.order_item.id} | Order Id :{self.order_item.order} | {self.order_item.quantity}"
        self.assertEqual(str(self.order_item), expected_str)

    def test_cost_calculation(self):
        expected_cost = self.order_item.quantity * self.product.price
        self.assertEqual(self.order_item.cost(), expected_cost)

    def test_cost_with_zero_quantity(self):
        # Create an order item with zero quantity
        order_item_zero_quantity = OrderItem.objects.create(order=self.order, product=self.product, quantity=0, customer=self.customer)
        self.assertEqual(order_item_zero_quantity.cost(), 0)

    def test_cost_with_large_quantity(self):
        # Create an order item with a large quantity
        order_item_large_quantity = OrderItem.objects.create(order=self.order, product=self.product, quantity=1000, customer=self.customer)
        expected_cost = order_item_large_quantity.quantity * self.product.price
        self.assertEqual(order_item_large_quantity.cost(), expected_cost)

    def test_cost_with_multiple_decimal_quantities(self):
        # Create an order item with a decimal quantity
        order_item_decimal_quantity = OrderItem.objects.create(order=self.order, product=self.product, quantity=1.5, customer=self.customer)
        expected_cost = order_item_decimal_quantity.quantity * self.product.price
        self.assertEqual(order_item_decimal_quantity.cost(), expected_cost)
        
class CustomOrderPermissionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.permission = CustomOrderPermission()
        self.request = self.client.get('/')
        self.view = None # In this case, we're not testing object permission, so the view isn't necessary

    def test_has_permission_for_post(self):
        # Test POST request
        self.request.method = 'POST'
        self.request.user = self.user
        self.assertTrue(self.permission.has_permission(self.request, self.view))

    def test_has_permission_for_get(self):
        # Test GET request
        self.request.method = 'GET'
        self.request.user = self.user
        self.assertTrue(self.permission.has_permission(self.request, self.view))

    def test_has_permission_for_other_methods(self):
        # Test other HTTP methods
        self.request.method = 'PUT'
        self.request.user = self.user
        self.assertTrue(self.permission.has_permission(self.request, self.view))
        
class OrderTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = get_user_model().objects.create_user(username='testuser', password='password123')
        self.admin_user = get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword', is_staff=True, role='Admin')
        self.category = Category.objects.create(title='Test Category')
        self.vendor = get_user_model().objects.create_user(username='vendor', email='vendor@example.com', password='vendorpassword', role='Vendor')
        self.product = Product.objects.create(title='Test Product', price=10, quantity=5, category=self.category, vendor=self.vendor)
    
    def test_create_order(self):
        self.client.force_authenticate(user=self.customer)
        data = {
            'customer': self.customer.id,
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(reverse('order-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
