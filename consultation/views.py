# django imports
from django.shortcuts import render, redirect

# project imports
from .models import Consultation
from appointment.models import Appointment
from .forms import ConsultationCreateForm
from employee.models import Employee

def save(request, id):
    logged_user = request.user
    doctor = Employee.objects.get(user=logged_user)
    ap = Appointment.objects.get(id=id)
    consultation = Consultation.objects.get(id=id)
    formCons = ConsultationCreateForm(request.POST, request.FILES, instance=consultation)
    if formCons.is_valid():
        formCons.save(commit=False)
        formCons.appointment = ap
        formCons.doctor = doctor
        formCons.creator = logged_user
        formCons.updater = logged_user
        formCons.save()
    else:
        print("Não valido!")
    return redirect('consultation:consultation', id)


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