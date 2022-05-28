from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('information/', views.information, name='information'),
]