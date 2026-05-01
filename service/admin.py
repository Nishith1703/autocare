from django.contrib import admin
from .models import Customer, Car, ServiceRecord

admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(ServiceRecord)
# Register your models here.
