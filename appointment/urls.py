# django imports
from django.urls import path

# project imports
from . import views


app_name = "appointment"

urlpatterns = [
    path('appointments_available/', views.getAppointmentsAvailable, name="appointments_available"),
    path('cancel/<str:pk>/', views.cancelAppointment, name="cancel_appointment"),
    path('customer_appointment/', views.customerAppointmentPage, name="customer_appointment"),
    path('employee_appointment/', views.employeeAppointmentPage, name="employee_appointment"),    
    path('employee_appointment/insert/', views.insertAppointment, name="employee_appointment_insert"),    
]