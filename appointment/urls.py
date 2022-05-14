from django.urls import path
from . import views


app_name = "appointment"

urlpatterns = [
    path('employee_appointment/', views.employeeAppointmentPage, name="employee_appointment"),
    path('doctor_by_specialty/', views.getDoctorBySpecialty, name="doctor_by_specialty"),
    path('employee_appointment/insert/', views.insertAppointment, name="employee_appointment_insert")
]