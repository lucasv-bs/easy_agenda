# django imports
from django.shortcuts import render

# project imports
from .models import Specialty


def specialtyList(request):
    context = {}
    return render(request, 'specialty_list.html', context)