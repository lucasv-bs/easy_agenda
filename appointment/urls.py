from django.urls import path
from . import views


app_name = "appointment"

urlpatterns = [
    path('employee_appointment/', views.employeeAppointmentPage, name="employee_appointment"),
    path('appointments_available/', views.getAppointmentsAvailable, name="appointments_available"),    
    path('employee_appointment/insert/', views.insertAppointment, name="employee_appointment_insert")
]