
from django.core.management.base import BaseCommand
from django_app.models import Product, Customer, Order

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Clear existing data
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        # Create Product entries
        product1 = Product.objects.create(
            name='Product A',
            price=19.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Product B',
            price=29.99,
            available=True
        )
        product3 = Product.objects.create(
            name='Product C',
            price=39.99,
            available=False
        )

        # Create Customer entries
        customer1 = Customer.objects.create(
            name='Illia',
            address='123 Wroclaw St'
        )
        customer2 = Customer.objects.create(
            name='Maryna',
            address='456 Warszawa St'
        )
        customer3 = Customer.objects.create(
            name='Dmytro',
            address='789 Kyiv St'
        )

        # Create Order entries
        order1 = Order.objects.create(
            customer=customer1,
            date='2024-11-06 10:00:00',
            status='New'
        )
        order2 = Order.objects.create(
            customer=customer2,
            date='2024-11-06 11:00:00',
            status='In Process'
        )
        order3 = Order.objects.create(
            customer=customer3,
            date='2024-11-06 12:00:00',
            status='Completed'
        )

        # Add products to orders
        order1.products.add(product1, product2)
        order2.products.add(product2, product3)
        order3.products.add(product1, product3)

        self.stdout.write("Data created successfully.")
