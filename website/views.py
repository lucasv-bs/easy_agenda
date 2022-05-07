# django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if usertype is None:
                messages.info(request, 'Enter your user type')
            else:
                login(request, user)
                if usertype == 'customer':
                    return redirect('customer:customer_home')
                if usertype == 'employee':
                    return redirect('employee')
        else:
            messages.info(request, 'Username or password is incorrect')
    
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('website:login')