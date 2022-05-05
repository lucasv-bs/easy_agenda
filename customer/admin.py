from django.contrib import admin

from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'cpf',
        'birth_date',
        'gender',
        'postal_code',
        'address',
        'address_number',
        'complement',
        'state',
        'city',
        'neighborhood',
        'tel1',
        'tel2',
        'active',
        'user',
        'creator',
        'updater',
        'created',
        'updated',
    ]