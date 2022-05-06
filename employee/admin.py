from django.contrib import admin


from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'cpf',
        'birth_date',
        'gender',
        'crm',
        'specialty',
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