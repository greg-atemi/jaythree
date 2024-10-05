from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(default="test@test.com")
    
class Product(models.Model):
    product_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    unit_price = models.IntegerField(default=0)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    sale_id = models.SmallAutoField(primary_key=True)
    code = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    total = models.IntegerField(default=0)
    tendered_amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    #customer_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.code
    
    @property
    def datetime(self):
        return datetime.combine(self.date, self.time)


class SaleItems(models.Model):
    saleItem_id = models.AutoField(primary_key=True)
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.saleItem_id}"
