from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)          
    name = models.CharField(max_length=100)          
    address = models.TextField()                     

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)        
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    available = models.BooleanField()                

    def __str__(self):
        return self.name


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
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) 

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"
