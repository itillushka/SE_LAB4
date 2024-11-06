from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)         
    name = models.CharField(max_length=255)          
    address = models.TextField()                     

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)          
    name = models.CharField(max_length=255)          
    price = models.FloatField()                      
    available = models.BooleanField()               

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)          
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    products = models.ManyToManyField(Product)      
    date = models.DateTimeField()                    
    status = models.CharField(max_length=50)        

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"
