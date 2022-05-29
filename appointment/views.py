# python imports
import json
from numpy import True_
import pandas
from datetime import date, datetime, timedelta
from time import strftime, time

# django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render

# project imports
from .models import Appointment
from clinic.models import Clinic
from consultation.models import Consultation
from customer.models import Customer
from employee.models import Employee
from specialty.models import Specialty
from website.decorators import allowed_users


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['customer'])
def customerAppointmentPage(request):
    specialty_list = Specialty.objects.all()

    context = {
        'specialty_list': specialty_list
    }
    return render(request, 'customer_appointment.html', context)


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['supervisor', 'attendant', 'doctor'])
def employeeAppointmentPage(request):
    customer_list = Customer.objects.all()
    specialty_list = Specialty.objects.all()

    context = {
        'customer_list': customer_list,
        'specialty_list': specialty_list
    }
    return render(request, 'employee_appointment.html', context)


#
# gets available appointments for the selected specialty and day
#
@login_required(login_url='website:login')
def getAppointmentsAvailable(request):
    requestBody = (dict(json.load(request)))

    appointment_date = requestBody['appointment_date']
    specialty_id = requestBody['specialty_id']

    if specialty_id is None:
        return HttpResponseNotFound(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment specialty was not informed.'
        }))
    if appointment_date is None:
        return HttpResponseNotFound(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment date was not informed.'
        }))

    appointments_available_json = {}

    specialty = Specialty.objects.get(id=specialty_id)
    doctors = Employee.objects.filter(
        specialty=specialty_id,
        active=True
    )

    if not doctors:
        return HttpResponseNotFound(JsonResponse({
            'status': 'warning',
            'message': 'No data found! No doctor registered for the informed specialty.'
        }))

    # get clinic data
    clinic = Clinic.objects.get(id=1)
    clinic_start_time = clinic.clinic_oppening
    clinic_end_time = clinic.clinic_closing
    consultation_duration = clinic.consultation_duration
    days_number_to_search = clinic.days_number_to_search

    clinic_start_time = clinic_start_time.strftime('%H:%M')
    clinic_end_time = clinic_end_time.strftime('%H:%M')
    consultation_duration = str(consultation_duration) + "min"    

    appointments_available_json = {
        "specialty_id": specialty.id,
        "specialty_name": specialty.name,
        "doctors": []
    }
    
    # search for appointments available for each doctor in the selected specialty and day
    for doctor in doctors:
        appointments_available_json['doctors'].append(
            getDoctorAvailability(
                doctor, appointment_date,
                clinic_start_time, clinic_end_time, 
                consultation_duration, days_number_to_search
            )
        )

    return JsonResponse(appointments_available_json)


# 
# gets available appointments from a doctor of the selected specialty
# 
def getDoctorAvailability(doctor, appointment_date, clinic_start_time, clinic_end_time, 
                consultation_duration, days_number_to_search):
    doctor_data = {
        "doctor_id": doctor.id,
        "doctor_name": doctor.name,
        "doctor_gender": doctor.gender,
        "doctor_crm": doctor.crm,
        "doctor_state": doctor.state,
        "selected_date": appointment_date,
        "available_times": []
    }
    # get the doctor's lunch time
    lunch_start_time = doctor.lunch_start_time
    lunch_finish_time = doctor.lunch_finish_time
    lunch_start_time = lunch_start_time.strftime('%H:%M')
    lunch_finish_time = lunch_finish_time.strftime('%H:%M')

    # get doctor's appointments
    doctor_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        status__in=['age', 'agu', 'ret'],
        canceled=False
    )

    # get a list of times
    time_list_before_luch = pandas.date_range(
        clinic_start_time, 
        lunch_start_time, 
        freq=consultation_duration
    ).time
    time_list_after_lunch = pandas.date_range(
        lunch_finish_time, 
        clinic_end_time, 
        freq=consultation_duration
    ).time
    # concatenate the lists using 'list comprehension'
    time_list = [y for x in [time_list_before_luch, time_list_after_lunch] for y in x]

    # Checks if the doctor has appointments for the selected date
    if doctor_appointments.count() > 0:
        # removes from the list of available times, all times that the doctor has appointments
        doctor_data["available_times"] = [i.strftime("%H:%M") for i in time_list if not i in doctor_appointments.values_list("appointment_time", flat=True)]
        
    else:
        # keeps the list of available times with all times of the day
        doctor_data["available_times"] = [i.strftime("%H:%M") for i in time_list]
        

    return doctor_data


#
# check for duplicate appointments
#
def checkDuplicateAppointments(appointment_date, customer, specialty):
    appointment = Appointment.objects.filter(
        appointment_date=appointment_date,
        customer=customer,
        specialty=specialty
    )

    return appointment.count() > 0


#
# register an appointment
#
@login_required(login_url='website:login')
def insertAppointment(request):
    data = (dict(json.load(request)))

    appointment_date = data['appointment_date']
    appointment_time = data['appointment_time']
    customer_id = data['customer_id']
    specialty_id = data['specialty_id']
    doctor_id = data['doctor_id']
    appointment_return = data['appointment_return']

    print(appointment_date, appointment_time, customer_id, specialty_id, doctor_id, appointment_return)

    if appointment_date is None or appointment_date == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment date was not informed.'
        }))
    
    if appointment_time is None or appointment_time == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment time was not informed.'
        }))
    
    if customer_id is None or customer_id == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment customer was not informed.'
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

    if appointment_return is None or appointment_return == '':
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! The appointment return was not informed.'
        }))
    
    
    if customer_id < 0:
        # the logged-in user is the customer
        customer = Customer.objects.get(user=request.user)
    else:
        # the employee selected a customer
        customer = Customer.objects.get(id=customer_id)

    specialty = Specialty.objects.get(id=specialty_id)
    doctor = Employee.objects.get(id=doctor_id)
    logged_user = request.user

    if checkDuplicateAppointments(appointment_date, customer, specialty):
        return HttpResponseBadRequest(JsonResponse({
            'status': 'error',
            'message': 'Invalid request! Duplicate records.'
        }))

    appointment = Appointment()
    appointment.appointment_date = appointment_date
    appointment.appointment_time = appointment_time
    appointment.appointment_return = appointment_return
    appointment.customer = customer
    appointment.specialty = specialty
    appointment.doctor = doctor
    appointment.justification = ''
    appointment.creator = logged_user
    appointment.updater = logged_user
    appointment.save()

    consultation = Consultation()
    consultation.appointment = appointment
    consultation.doctor = doctor
    consultation.updater = logged_user
    consultation.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Appointment successfully registered'
    })


@login_required(login_url='website:login')
def cancelAppointment(request):
    data = (dict(json.load(request)))
    if data['id'] is None or data['id'] == '':
        return {
            'status': 'error',
            'message': 'Invalid request! The appointment id was not informed.'
        }
    id = data['id']
    appointment = Appointment.objects.get(id=id)
    appointment.canceled = True
    appointment.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Appointment Canceled'
    })


def getListByCanceled(request, data):
    customer = Customer.objects.get(user=request.user)
    appointment_list = Appointment.objects.filter(canceled = False, customer=customer)
    r = []
    for x in appointment_list:
        r += {
            "id" : x.id,
            "date" : x.date,
            "hour" : x.hour,
            "customer" : customer.__str__(),
            "doctor" : x.doctor.__str__(),
            "specialty" : x.specialty.__str__(),
            "status" : x.status,
            "canceled" : x.canceled,
        },
    return r


def getListByDate(request, data):
    if data['day'] is None or data['day'] == '':
        return {
            'status': 'error',
            'message': 'Invalid request! The appointment date was not informed.'
        }
    customer = Customer.objects.get(user=request.user)
    appointment_list = Appointment.objects.filter(date=data['day'], customer=customer)
    r = []
    for x in appointment_list:
        r += {
            "id" : x.id,
            "date" : x.date,
            "hour" : x.hour,
            "customer" : customer.__str__(),
            "doctor" : x.doctor.__str__(),
            "specialty" : x.specialty.__str__(),
            "status" : x.status,
            "canceled" : x.canceled,
        },
    
    return r
    

def filter(request):
    data = dict(json.load(request))
    if (data['filter'] == '1'):
        return JsonResponse(getListByDate(request, data), safe=False)
    elif (data['filter'] == '2'):
        return JsonResponse(getListByCanceled(request, data), safe=False)
    else:
        return JsonResponse({'status' : 'error',
            'message' : 'Invalid request! Chose one of the filters.'}, safe=False)