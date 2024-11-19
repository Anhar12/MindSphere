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
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Sign up successful!'
            })

        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list

            return JsonResponse({
                'status': 'error',
                'message': 'Sign up failed.',
                'errors': errors
            })

    return render(request, 'Home/sign-up.html', {'section': 'sign-in'})

def SignOut(request):
    logout(request)
    return redirect('sign-in')

def Dashboard(request):
    return render(request, 'MindSphere/dashboard.html', context={'section' : 'dashboard'})

def TestSchedule(request):
    return render(request, 'MindSphere/schedule.html', context={'section' : 'test-schedule'})

def PsychologicalTest(request):
    return render(request, 'MindSphere/test.html', context={'section' : 'psychological-test'})

def PsycologistManagement(request):
    return render(request, 'MindSphere/psychologist.html', context={'section' : 'psychologist'})

def History(request):
    return render(request, 'MindSphere/history.html', context={'section' : 'history'})