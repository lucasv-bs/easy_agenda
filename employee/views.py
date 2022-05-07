# django imports
from django.shortcuts import render

# project imports
from .models import Employee


def employeePage(request):
    context = {}
    return render(request, 'employee.html', context)