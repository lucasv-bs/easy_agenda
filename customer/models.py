from django.db import models

from users.models import User


class Customer(models.Model):
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
    postal_code = models.CharField(max_length=8)
    address = models.CharField(max_length=150)
    address_number = models.CharField(max_length=7)
    complement = models.CharField(max_length=70, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_LIST)
    city = models.CharField(max_length=150)
    neighborhood = models.CharField(max_length=150)
    tel1 = models.CharField(max_length=11)
    tel2 = models.CharField(max_length=11, blank=True, null=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer')
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='customer_creator_set')
    updater = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name='customer_updater_set')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
