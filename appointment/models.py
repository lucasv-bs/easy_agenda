from django.db import models

from users.models import User
from customer.models import Customer
from employee.models import Employee
from specialty.models import Specialty

class Appointment(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    appointment_return = models.BooleanField(default=False)    
    canceled = models.BooleanField(default=False)
    justification = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='appointment_creator_set')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Employee, on_delete=models.PROTECT)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
    updater = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='appointment_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)