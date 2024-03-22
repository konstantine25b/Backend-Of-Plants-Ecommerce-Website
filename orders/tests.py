from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem, Product
from products.models import Category
from decimal import Decimal

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