from inspect import GEN_CLOSED
from django.db import models
from django.forms import BooleanField


from users.models import User
from specialty.models import Specialty


class Employee(models.Model):
    GENDER_OPTIONS = (
        ('m', 'Masculino'),
        ('f', 'Feminino'),
        ('o', 'Outros'),
    )

    STATE_LIST = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceara'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11)    
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    crm = models.CharField(max_length=13, blank=True, null=True)
    postal_code = models.CharField(max_length=8)
    address = models.CharField(max_length=150)
    address_number = models.CharField(max_length=7)
    complement = models.CharField(max_length=70, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_LIST)
    city = models.CharField(max_length=150)
    neighborhood = models.CharField(max_length=150)
    tel1 = models.CharField(max_length=11)
    tel2 = models.CharField(max_length=11, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    finish_time = models.TimeField(blank=True, null=True)
    lunch_start_time = models.TimeField(blank=True, null=True)
    lunch_finish_time = models.TimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    specialty = models.ForeignKey(Specialty, blank=True, null=True, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='employee_creator_set')
    updater = models.ForeignKey(User, on_delete=models.PROTECT, related_name='employee_updater_set')

    
    class Meta:
        ordering = ("start_time", "name",)


    def __str__(self):
        return self.name