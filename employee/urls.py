# django imports
from django.urls import path
from . import views
from appointment import views as appointment_view

app_name = "employee"

urlpatterns = [
    path('', views.employeePage, name="employee_home"),
    path('cancel_appointment/', appointment_view.cancelAppointment, name='cancel-appointment')
]