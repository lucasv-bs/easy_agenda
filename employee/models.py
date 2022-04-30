from django.db import models
from django.forms import BooleanField


from users.models import User
from specialty.models import Specialty


class Employee(models.Model):
    name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11)    
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)
    crm = models.CharField(max_length=13, null=True)
    postal_code = models.CharField(max_length=8)
    address = models.CharField(max_length=150)
    address_number = models.CharField(max_length=7)
    complement = models.CharField(max_length=70, null=True)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=150)
    neighborhood = models.CharField(max_length=150)
    tel1 = models.CharField(max_length=11)
    tel2 = models.CharField(max_length=11, null=True)    
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    specialty = models.ForeignKey(Specialty, null=True, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='employee_creator_set')
    updater = models.ForeignKey(User, on_delete=models.PROTECT, related_name='employee_updater_set')
