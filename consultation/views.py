# django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# project imports
from .models import Consultation
from appointment.models import Appointment
from .forms import ConsultationCreateForm
from employee.models import Employee
from website.decorators import allowed_users


def save(request, id):
    logged_user = request.user
    doctor = Employee.objects.get(user=logged_user)
    ap = Appointment.objects.get(id=id)
    consultation = Consultation.objects.get(id=id)
    customer = ap.customer
    formCons = ConsultationCreateForm(request.POST, request.FILES, instance=consultation)
    if formCons.is_valid():
        formCons.appointment = ap
        formCons.doctor = doctor
        formCons.creator = logged_user
        formCons.updater = logged_user
        formCons.save()
    else:
        print("Não valido!")
    return redirect('consultation:consultation', id)


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['supervisor', 'doctor'])
def consultation(request, id):
    appointment = Appointment.objects.get(id=id)
    consultation = Consultation.objects.get(appointment=appointment)
    consultation_form = ConsultationCreateForm
    context = {
        'consultation_form' : consultation_form,
        'consultation': consultation,
        'appointment': appointment
    }
    
    return render(request, 'consultation.html', context)