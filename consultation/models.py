from django.db import models
import appointment

from appointment.models import Appointment
from employee.models import Employee
from users.models import User


class Consultation(models.Model):
    medical_chart = models.FileField(blank=True, null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Employee, on_delete=models.PROTECT)
    updater = models.ForeignKey(User, on_delete=models.PROTECT)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)