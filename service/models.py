from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)

    def __str__(self):
        return self.car_name


class ServiceRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_date = models.DateField()
    description = models.TextField()
    cost = models.IntegerField()

    def __str__(self):
        return self.description

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.service_type# Create your models here.
