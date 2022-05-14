# django imports
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import json

# project imports
from .models import Appointment
from customer.models import Customer
from employee.models import Employee
from specialty.models import Specialty


def employeeAppointmentPage(request):
    customer_list = Customer.objects.all()
    specialty_list = Specialty.objects.all()

    context = {
        'customer_list': customer_list,
        'specialty_list': specialty_list
    }
    return render(request, 'employee_appointment.html', context)


def getDoctorBySpecialty(request):
    data = dict(json.load(request))
    
    specialty_id = data['specialty_id']
    if specialty_id is None:
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The specialty was not informed'
        }))
    
    specialty = Specialty.objects.get(id=specialty_id)
    employee_list = Employee.objects.filter(specialty=specialty)
    
    if not employee_list:
        return HttpResponseNotFound(JsonResponse({
            'status': 'warning',
            'message': 'No data found! No doctor registered for the informed specialty.'
        }))

    employee_list_json = {}
    for employee in employee_list:
        employee_list_json[employee.id] = employee.name

    return JsonResponse(employee_list_json)


def insertAppointment(request):
    data = (dict(json.load(request)))

    date = data['date']
    hour = data['hour']
    customer_id = data['customer_id']
    specialty_id = data['specialty_id']
    doctor_id = data['doctor_id']

    if date is None or date == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment date was not informed.'
        }))
    
    if hour is None or hour == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment hour was not informed.'
        }))
    
    if customer_id is None or customer_id == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment customer_id was not informed.'
        }))
    
    if specialty_id is None or specialty_id == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment specialty was not informed.'
        }))
    
    if doctor_id is None or doctor_id == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment doctor was not informed.'
        }))

    customer = Customer.objects.get(id=customer_id)
    specialty = Specialty.objects.get(id=specialty_id)
    doctor = Employee.objects.get(id=doctor_id)
    logged_user = request.user

    appointment = Appointment()
    appointment.date = date
    appointment.hour = hour
    appointment.customer = customer
    appointment.specialty = specialty
    appointment.doctor = doctor
    appointment.justification = ''
    appointment.creator = logged_user
    appointment.updater = logged_user

    appointment.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Appointment successfully registered'
    })