# django imports
from django.shortcuts import render

# project imports
from .models import Specialty


def specialtyList(request):
    specialty_list = Specialty.objects.filter(active=True)
    context = {"specialty_list" : specialty_list}
    return render(request, 'specialty_list.html', context)