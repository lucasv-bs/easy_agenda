# django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_staff:
                return redirect('employee:employee_home')
            else:
                return redirect('customer:customer_home')
        else:
            messages.info(request, 'Username or password is incorrect')
    
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)    
    return redirect('website:login')