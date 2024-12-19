from django.test import TestCase
from django_app.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):

    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=-1.99, available=True)
            temp_product.full_clean()

    def test_create_product_without_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_without_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='No price product', price=None, available=True)
            temp_product.full_clean()

    def test_create_product_without_available(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='No available product', price=1.99, available=None)
            temp_product.full_clean()

    def test_create_product_with_edge_name_length(self):
        max_length_name = 'a' * 255
        temp_product = Product.objects.create(name=max_length_name, price=1.99, available=True)
        self.assertEqual(temp_product.name, max_length_name)

    def test_create_product_with_edge_price_value(self):
        min_price_product = Product.objects.create(name='Min price product', price=0.01, available=True)
        self.assertEqual(min_price_product.price, 0.01)

        max_price_product = Product.objects.create(name='Max price product', price=9999999.99, available=True)
        self.assertEqual(max_price_product.price, 9999999.99)

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid price format', price=1.999, available=True)
            temp_product.full_clean()

class CustomerModelTest(TestCase):

    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.assertEqual(temp_customer.name, 'John Doe')
        self.assertEqual(temp_customer.address, '123 Main St')

    def test_create_customer_without_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='', address='123 Main St')
            temp_customer.full_clean()

    def test_create_customer_without_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='John Doe', address='')
            temp_customer.full_clean()

    def test_create_customer_with_edge_name_length(self):
        max_length_name = 'a' * 100
        temp_customer = Customer.objects.create(name=max_length_name, address='123 Main St')
        self.assertEqual(temp_customer.name, max_length_name)

class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.product1 = Product.objects.create(name='Product 1', price=10.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, available=False)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'New')
        self.assertIn(self.product1, order.products.all())

    def test_create_order_without_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=None, status='New')
            order.full_clean()

    def test_create_order_without_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status=None)
            order.full_clean()
    
    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status='InvalidStatus')
            order.full_clean()

    def test_total_price_calculation_with_valid_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 30.00)

    def test_total_price_calculation_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        total_price = sum(product.price for product in order.products.all())
        self.assertEqual(total_price, 0.00)

    def test_order_fulfillment_with_product_availability(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        can_fulfill = all(product.available for product in order.products.all())
        self.assertFalse(can_fulfill)

        order.products.remove(self.product2)
        can_fulfill = all(product.available for product in order.products.all())
        self.assertTrue(can_fulfill)