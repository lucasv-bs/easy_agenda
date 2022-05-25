# django imports
from django.urls import path

# project imports
from . import views

app_name = "consultation"

urlpatterns = [
    path('', views.consultation, name='consultation')
]