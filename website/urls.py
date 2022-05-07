from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.loginPage, name='logout')
]