from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    
    path('car/add/', views.add_car, name='add_car'),
    path('car/edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('car/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    
    path('service/book/', views.book_service, name='book_service'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
]