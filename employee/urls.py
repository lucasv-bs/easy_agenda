# django imports
from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path('', views.employeePage, name="employee_home")
]