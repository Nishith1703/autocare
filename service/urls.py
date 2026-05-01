from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.customer_dashboard, name="customer_dashboard"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("add-car/", views.add_car, name="add_car"),
    path("book-service/", views.book_service, name="book_service"),
    path("edit-car/<int:car_id>/", views.edit_car, name="edit_car"),
path("delete-car/<int:car_id>/", views.delete_car, name="delete_car"),

path("edit-service/<int:service_id>/", views.edit_service, name="edit_service"),
path("delete-service/<int:service_id>/", views.delete_service, name="delete_service"),
]