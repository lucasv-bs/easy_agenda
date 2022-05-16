# django imports
from django.contrib import admin

# project imports
from .models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = [
        'clinic_oppening',
        'clinic_closing',
        'duration_consultation'
    ]