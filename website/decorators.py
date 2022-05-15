from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('employee:employee_home')
            else:
                return redirect('customer:customer_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
