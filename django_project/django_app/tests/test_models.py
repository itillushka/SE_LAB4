from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django_app.models import Product, Customer, Order
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

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
        self.product1 = Product.objects.create(name='Product 1222', price=10.00, available=True)
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

class ProductApiTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')
        self.product = Product.objects.create(name='Temporary Product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product.id])

    def test_get_all_products_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_all_products_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary Product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_single_product_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary Product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_get_single_product_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary Product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_create_product_with_valid_data_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_valid_data_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Temporary Product 2')
        self.assertEqual(response.data['price'], '4.99')
        self.assertTrue(response.data['available'])

    def test_modify_product_with_valid_data_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_product_with_valid_data_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Modified Product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_delete_product_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class ProductApiNegativeTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')
        self.product = Product.objects.create(name='Temporary Product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product.id])
        self.invalid_product_detail_url = reverse('product-detail', args=[999])

    def test_create_product_with_invalid_data_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "", "price": -1, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_invalid_data_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "", "price": -1, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_nonexistent_product_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.invalid_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nonexistent_product_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.invalid_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_modify_product_with_invalid_data_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "", "price": -1}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_product_with_invalid_data_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {"name": "", "price": -1}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_product_as_regular_user(self):
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.invalid_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_product_as_admin(self):
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(self.invalid_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)