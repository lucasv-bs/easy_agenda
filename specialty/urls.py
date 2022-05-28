# django imports
from django.urls import path

# project imports
from . import views


app_name = 'specialty'

urlpatterns = [
    path('', views.specialtyList, name='specialty_list')
]