# django imports
from django.shortcuts import render

import customer

# project imports
from .forms import CustomerCreateForm, UserCustomerCreateForm


def registerPage(request):
    form_customer = CustomerCreateForm()
    form_user = UserCustomerCreateForm()

    if request.method == 'POST':
        form_customer = CustomerCreateForm(request.POST)
        form_user = UserCustomerCreateForm(request.POST)

        if form_customer.is_valid() and form_user.is_valid():
            user = form_user.save()
            
            customer = form_customer.save(commit=False)
            customer.user = user
            customer.save()

    context = {'form_customer': form_customer, 'form_user': form_user}
    return render(request, 'register.html', context)