from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import SignUpForm
from .models import Registrations, Users, Results, TestSchedules
from django.db.models import Q

def Home(request):
    context = {
        'section' : 'home'
    }
    return render(request, 'Home/index.html', context)

def About(request):
    context = {
        'section' : 'about'
    }
    return render(request, 'Home/about.html', context)

def Contact(request):
    context = {
        'section' : 'contact'
    }
    return render(request, 'Home/contact.html', context)

def SignIn(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    
    context = {
        'section' : 'sign-in'
    }
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Sign in successfuly!',
                'role' : user.role,
                'isAdmin' : user.is_staff
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password.',
            })

    return render(request, 'Home/sign-in.html', context)

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Sign up successful!'
            })
        else:
            errors = {}
            for field, messages in form.errors.items():
                errors[field] = messages
 
            return JsonResponse({
                'status': 'error',
                'message': errors
            })

    else:
        form = SignUpForm()
    return render(request, 'Home/sign-up.html', {'form': form, 'section' : 'sign-in'})

def SignOut(request):
    logout(request)
    return redirect('sign-in') 