from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer, Car, ServiceBooking
from .forms import CarForm, ServiceBookingForm


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


def customer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()

    if customer is None:
        return render(request, "customer_dashboard.html", {
            "customer": None,
            "cars": [],
            "services": [],
            "message": "No customer profile found. Please ask admin to create your customer profile."
        })

    cars = Car.objects.filter(customer=customer)
    services = ServiceBooking.objects.filter(customer=customer)

    return render(request, "customer_dashboard.html", {
        "customer": customer,
        "cars": cars,
        "services": services
    })
    
def add_car(request):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()

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


def book_service(request):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()

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

def edit_car(request, car_id):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()
    car = Car.objects.get(id=car_id, customer=customer)

    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
    else:
        form = CarForm(instance=car)

    return render(request, "add_car.html", {"form": form})


def delete_car(request, car_id):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()
    car = Car.objects.get(id=car_id, customer=customer)
    car.delete()

    return redirect("customer_dashboard")


def edit_service(request, service_id):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()
    service = ServiceBooking.objects.get(id=service_id, customer=customer)

    if request.method == "POST":
        form = ServiceBookingForm(request.POST, instance=service)
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
    else:
        form = ServiceBookingForm(instance=service)
        form.fields["car"].queryset = Car.objects.filter(customer=customer)

    return render(request, "book_service.html", {"form": form})


def delete_service(request, service_id):
    if not request.user.is_authenticated:
        return redirect("login")

    customer = Customer.objects.filter(user=request.user).first()
    service = ServiceBooking.objects.get(id=service_id, customer=customer)
    service.delete()

    return redirect("customer_dashboard")