# django imports
from django.contrib import admin

# project imports
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = [
        'status',
        'medical_chart',
        'appointment',
        'doctor',
        'updater',
        'created',
        'updated'
    ]