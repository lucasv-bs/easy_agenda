# python imports
from time import strftime, time

# django imports
from django.db import models

# project imports
from users.models import User
from customer.models import Customer
from employee.models import Employee
from specialty.models import Specialty

class Appointment(models.Model):

    APPOINTMENT_STATUS = (
        ('nac', 'Não compareceu'),
        ('age', 'Agendado'),
        ('agu', 'Aguardando'),
        ('can', 'Cancelado'),
        ('ret', 'Retorno'),
        ('fin', 'Finalizado'),
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_return = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    justification = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=100, default='age', choices=APPOINTMENT_STATUS)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='appointment_creator_set')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Employee, on_delete=models.PROTECT)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
    updater = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='appointment_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ("appointment_date", "appointment_time", "specialty", "doctor", "customer",)

    
    def __str__(self):
        return self.specialty.name + '-' + self.appointment_date.strftime("%d/%m/%Y") + '-' + self.appointment_time.strftime('%H:%M')