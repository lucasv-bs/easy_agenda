# python imports
from datetime import date

# django imports
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# project imports
from .models import Employee
from appointment.models import Appointment
from website.decorators import allowed_users


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['supervisor', 'attendant', 'doctor'])
def employeePage(request):
    user_group = request.user.groups.all()[0].name

    employee = Employee.objects.get(user=request.user)
    
    if user_group == 'attendant':
        return attendantPage(request, employee)
    if user_group == 'doctor':
        return doctorPage(request, employee)
    if user_group == 'supervisor':
        return supervisorPage(request, employee)


def attendantPage(request, employee):
    appointment_list = Appointment.objects.filter(date=date.today(), canceled=False)
    total_appointments = appointment_list.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(appointment_list, 5)
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)        

    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'employee': employee
    }
    return render(request, 'attendant_home.html', context)


def doctorPage(request, employee):
    context = {}
    return render(request, 'employee.html', context)


def supervisorPage(request, employee):
    context = {}
    return render(request, 'employee.html', context)