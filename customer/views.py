# django imports
from django.shortcuts import render

import customer

# project imports
from .forms import CustomerCreateForm, UserCustomerCreateForm
from .models import Customer
from users.models import User


def registerPage(request):
    form_customer = CustomerCreateForm()
    form_user = UserCustomerCreateForm()

    if request.method == 'POST':
        form_customer = CustomerCreateForm(request.POST)
        form_user = UserCustomerCreateForm(request.POST)

        if form_customer.is_valid() and form_user.is_valid():
            user = form_user.save()
            
            print(user)

            customer = form_customer.save(commit=False)
            customer.user = user
            customer.save()
            
            print(customer)

    context = {'form_customer': form_customer, 'form_user': form_user}
    return render(request, 'register.html', context)