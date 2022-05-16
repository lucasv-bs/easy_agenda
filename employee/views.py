# django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# project imports
from .models import Employee
from website.decorators import allowed_users


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['admin', 'attendant', 'doctor'])
def employeePage(request):
    context = {}
    return render(request, 'employee.html', context)