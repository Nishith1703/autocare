from django import forms
from .models import Car, ServiceBooking

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_name', 'car_number']


class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['car', 'service_type', 'service_date']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'})
        }