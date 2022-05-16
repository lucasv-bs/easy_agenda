# django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# project imports
from .forms import CustomerCreateForm, UserCustomerCreateForm
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

            customer = form_customer.save(commit=False)
            customer.user = user
            customer.save()
            
            messages.success(request, 'Usuário ' + username + ' registrado com sucesso.')
            return redirect('website:login')

    context = {'form_customer': form_customer, 'form_user': form_user}
    return render(request, 'register.html', context)


@login_required(login_url='website:login')
@allowed_users(allowed_roles=['customer'])
def customerPage(request):
    context = {}
    return render(request, 'customer.html', context)