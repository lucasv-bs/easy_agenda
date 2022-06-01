# python imports
from datetime import date, datetime

# django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

# project imports
from .forms import CustomerCreateForm, UserCustomerCreateForm
from .models import Customer
from appointment.models import Appointment
from website.decorators import allowed_users


def registerPage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('customer:customer_home')

    form_customer = CustomerCreateForm()
    form_user = UserCustomerCreateForm()

    if request.method == 'POST':
        form_customer = CustomerCreateForm(request.POST)
        form_user = UserCustomerCreateForm(request.POST)

        if form_customer.is_valid() and form_user.is_valid():
            user = form_user.save()
            username = form_user.cleaned_data.get('username')

            # set group to the customer
            customerGroup = Group.objects.get(name='customer')
            user.groups.add(customerGroup)

            logged_user = None
            if request.user.is_staff:
                logged_user = request.user
            else:
                logged_user = user

            customer = form_customer.save(commit=False)
            customer.user = user
            customer.creator = logged_user
            customer.updater = logged_user
            customer.save()
            
            messages.success(request, 'Usuário ' + username + ' registrado com sucesso.')
            return redirect('website:login')

    context = {'form_customer': form_customer, 'form_user': form_user}
    return render(request, 'register.html', context)


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['customer'])
def customerPage(request):
    customer = Customer.objects.get(user=request.user)
    appointment_list = Appointment.objects.filter(
        customer=customer,
        appointment_date__gte=datetime.now().date(),
        status__in=['age', 'agu', 'ret'],
        canceled=False
    )
    total_appointments = appointment_list.count()

    context = {
        'customer': customer,
        'appointment_list': appointment_list,
        'total_appointments': total_appointments
    }
    return render(request, 'customer.html', context)