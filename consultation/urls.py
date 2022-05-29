# django imports
from django.urls import path

# project imports
from . import views

app_name = "consultation"

urlpatterns = [
    path('<int:id>/', views.consultation, name='consultation'),
    path('<int:id>/save/', views.save, name='save-consultation')
]