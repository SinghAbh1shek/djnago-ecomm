from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(first_name, last_name, username, email, password)
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            messages.error(request, "Error: Username or email already exist")
            return redirect('/accounts/registration/')
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Success: Account Created")
        return redirect('/')

    return render(request, 'registration.html')

def login_page(request):


    
    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.error(request, "Error: Username does not exist")
            return redirect('/')
        
        user_obj = authenticate(username = username, password=password)
        if not user_obj:
            messages.error(request, "Error: Invalid Credentials")
            return redirect('/')
        
        login(request, user_obj)
        return redirect('/')
        
    return redirect('/')

def logout_page(request):
    logout(request)
    messages.error(request, "Success: Logged Successfully")
    return redirect('/')

