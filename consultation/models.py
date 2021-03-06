# django imports
from datetime import date
from django.db import models
import os

# project imports
from appointment.models import Appointment
from employee.models import Employee
from users.models import User


class Consultation(models.Model):

    

    def get_upload_path(instance, file):
        t = os.path.join(
            "medical_charts/",
            str(instance.appointment.customer.id),
            str(instance.appointment.appointment_date),
            file
        )
        return str(t)


    CONSULTATION_STATUS = (
        ('pen', 'Pendente'),
        ('eat', 'Em andamento'),
        ('fin', 'Finalizado'),
    )

    
    #"static/medical_charts/"

    medical_chart = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    status = models.CharField(max_length=100, default='pen', choices=CONSULTATION_STATUS)
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Employee, on_delete=models.PROTECT)
    updater = models.ForeignKey(User, on_delete=models.PROTECT)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return 'Consultation-' + self.status