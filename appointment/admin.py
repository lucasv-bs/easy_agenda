# django imports
from django.contrib import admin

# project imports
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'date', 
        'hour',
        'customer',
        'specialty',
        'doctor',
        'appointment_return',
        'canceled',
        'justification',
        'active',
        'creator',
        'updater',
        'created',
        'updated',
    ]