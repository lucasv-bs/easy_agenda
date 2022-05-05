# django imports
from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

# project imports
from .models import Customer
from users.models import User


class CustomerCreateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['active', 'user', 'creator', 'updater', 'created', 'updated']


class UserCustomerCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']