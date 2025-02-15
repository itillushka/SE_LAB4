from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)          
    address = models.TextField()                     

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.name:
            raise ValidationError('Name must be specified.')
        if not self.address:
            raise ValidationError('Address must be specified.')
        super().save(*args, **kwargs)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)          
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    available = models.BooleanField()                

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        if self.price is None or self.price <= 0:
            raise ValidationError('Price must be a positive number.')
        if self.available is None:
            raise ValidationError('Availability must be specified.')
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed')
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

    def calculate_total_price(self):
        total_price = self.products.aggregate(total=Sum('price'))['total'] or 0
        return total_price

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())