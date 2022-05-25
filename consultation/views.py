# django imports
from django.shortcuts import render

# project imports
from .models import Consultation
from appointment.models import Appointment


def consultation(request):
    consultation = Consultation.objects.get(id=2)
    appointment = Appointment.objects.get(id=consultation.appointment.id)
    
    context = {
        'consultation': consultation,
        'appointment': appointment
    }
    
    return render(request, 'consultation.html', context)