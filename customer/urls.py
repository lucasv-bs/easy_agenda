from django.urls import path

from . import views

app_name = "customer"

urlpatterns = [
    path('', views.customerPage, name="customer_home"),
    path('register/', views.registerPage, name="customer_register")
]