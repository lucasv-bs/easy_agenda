# django imports
from django.contrib import admin

# project imports
from .models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = [
        'clinic_oppening',
        'clinic_closing',
        'consultation_duration',
        'days_number_to_search'
    ]