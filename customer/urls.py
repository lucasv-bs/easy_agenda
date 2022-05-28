# django imports
from django.urls import path

# project imports
from . import views
from appointment import views as appointment_view


app_name = "customer"

urlpatterns = [
    path('', views.customerPage, name="customer_home"),
    path('register/', views.registerPage, name="customer_register"),
    path('cancel_appointment/', appointment_view.cancelAppointment, name="cancel_appointment"),
]