from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer, Car, ServiceBooking
from .forms import CarForm, ServiceBookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

def forgot_password(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            message = "Password reset successful. You can login now."
        except User.DoesNotExist:
            message = "User not found"

    return render(request, "forgot_password.html", {"message": message})

@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
            "phone": "",
            "address": "",
        }
    )

    message = ""

    if request.method == "POST":
        customer.name = request.POST.get("name")
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        customer.save()

        new_password = request.POST.get("new_password")
        if new_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

        message = "Profile updated successfully"

    return render(request, "profile.html", {
        "customer": customer,
        "message": message
    })

def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("customer_dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})

def signup_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            Customer.objects.create(
                user=user,
                name=name,
                phone=phone,
                email=email,
                address=address
            )

            login(request, user)
            return redirect("customer_dashboard")

    return render(request, "signup.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def customer_dashboard(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
            "phone": "",
            "address": "",
        }
    )

    cars = Car.objects.filter(customer=customer)
    services = ServiceBooking.objects.filter(customer=customer)

    return render(request, "customer_dashboard.html", {
        "customer": customer,
        "cars": cars,
        "services": services
    })

@login_required
def add_car(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
            "phone": "",
            "address": "",
        }
    )

    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.customer = customer
            car.save()
            return redirect("customer_dashboard")
    else:
        form = CarForm()

    return render(request, "add_car.html", {"form": form})

@login_required
def edit_car(request, car_id):
    customer = get_object_or_404(Customer, user=request.user)
    car = get_object_or_404(Car, id=car_id, customer=customer)

    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
    else:
        form = CarForm(instance=car)

    return render(request, "add_car.html", {"form": form, "is_edit": True})

@login_required
def delete_car(request, car_id):
    customer = get_object_or_404(Customer, user=request.user)
    car = get_object_or_404(Car, id=car_id, customer=customer)
    
    if request.method == "POST":
        car.delete()
        return redirect("customer_dashboard")
        
    return render(request, "confirm_delete_car.html", {"car": car})

@login_required
def book_service(request):
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == "POST":
        form = ServiceBookingForm(request.POST)
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

        if form.is_valid():
            service = form.save(commit=False)
            service.customer = customer
            service.cost = 0
            service.status = "Pending"
            service.save()
            return redirect("customer_dashboard")
    else:
        form = ServiceBookingForm()
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

    return render(request, "book_service.html", {"form": form})

@login_required
def edit_service(request, service_id):
    customer = get_object_or_404(Customer, user=request.user)
    service = get_object_or_404(ServiceBooking, id=service_id, customer=customer)

    if request.method == "POST":
        form = ServiceBookingForm(request.POST, instance=service)
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
    else:
        form = ServiceBookingForm(instance=service)
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

    return render(request, "book_service.html", {"form": form, "is_edit": True})

@login_required
def delete_service(request, service_id):
    customer = get_object_or_404(Customer, user=request.user)
    service = get_object_or_404(ServiceBooking, id=service_id, customer=customer)
    
    if request.method == "POST":
        service.delete()
        return redirect("customer_dashboard")
        
    return render(request, "confirm_delete_service.html", {"service": service})