from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_required, login_required, user_required, ParticipantPsychologist_required
from django.http import JsonResponse
from .forms import SignUpForm, ScheduleForm
from .models import Registrations, Users, Results, TestSchedules
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count, F
import os

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

@login_required()
def Dashboard(request):
    return render(request, 'MindSphere/dashboard.html', context={'section' : 'dashboard'})

def delete_old_file(file_path):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

@login_required()
def TestSchedule(request):
    psychologists = Users.objects.filter(role=Users.PSYCHOLOGIST)
    today = now().date()
    tomorrow = today + timedelta(days=1)
    
    schedules = TestSchedules.objects.annotate(
        registered_count=Count('registrations')
    ).filter(
        Date__gte=tomorrow,
        registered_count__lt=F('Capacity')
    ).order_by('Date')
    
    if request.user.role == -1:
        return render(request, 'MindSphere/schedule.html', context={
            'section' : 'test-schedule', 
            'psychologists' : psychologists,
            'test_schedules' : schedules,
        })
    
    return render(request, 'MindSphere/schedule.html', context={
        'section' : 'test-schedule',
        'test_schedules' : schedules,
    })

@admin_required()
def AddSchedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            schedule = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Schedule added successfully!'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
                
            return JsonResponse({
                'status': 'error',
                'message': 'Failed adding schedule! please check your input',
                'errors': errors,
            })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method!',
    })
    
@admin_required()
def UpdateSchedule(request, pk):
    if request.method == 'POST':
        schedule = TestSchedules.objects.filter(id=pk).first()
        
        if not schedule:
            return JsonResponse({
                'status': 'error',
                'message': 'Test schedule not found!'
            })
        
        form = ScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            schedule.Name = data['Name']
            psychologist_id = data['Psychologist']
            psychologist = Users.objects.filter(id=psychologist_id.id, role=Users.PSYCHOLOGIST).first()
            if not psychologist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Selected psychologist is invalid!'
                })
            schedule.Psychologist = psychologist
            
            schedule.Description = data['Description']
            schedule.Date = data['Date']
            schedule.Capacity = data['Capacity']
            schedule.Location = data['Location']
            
            if 'Image' in request.FILES:
                if schedule.Image:
                    delete_old_file(schedule.Image.path)
                schedule.Image = request.FILES['Image']
                
            try:
                schedule.save()
            except ValidationError as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Invalid Data: {str(e)}'
                })
            
            return JsonResponse({
                'status': 'success',
                'message': 'Schedule updated successfully!'
            })
            
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
                
            return JsonResponse({
                'status': 'error',
                'message': 'Failed updating schedule! please check your input',
                'errors': errors,
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@admin_required()
def DeleteSchedule(request, pk):
    if request.method == 'DELETE':
        try:
            schedule = TestSchedules.objects.get(id=pk)
            if schedule.Image:
                delete_old_file(schedule.Image.path)
            schedule.delete()
            return JsonResponse({'status': 'success', 'message': 'Schedule deleted successfully!'})
        except TestSchedules.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Schedule not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@user_required()
def RegisterSchedule(request, pk):
    if request.method == 'POST':
        schedule = TestSchedules.objects.filter(id=pk).first()
        print(schedule)
        if not schedule:
            return JsonResponse({
                'status': 'error',
                'message': 'Test schedule not found!'
            })

        if Registrations.objects.filter(User=request.user, TestSchedule=schedule).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'You have already registered for this schedule!'
            })
        
        total_registered = Registrations.objects.filter(TestSchedule=schedule).count()
        if total_registered >= schedule.Capacity:
            return JsonResponse({
                'status': 'error',
                'message': 'Test schedule has reached its maximum capacity.'
            })
        
        registration = Registrations(User=request.user, TestSchedule=schedule)
        registration.save()
        
        return JsonResponse({'status': 'success', 'message': 'Registration successful!'})

@ParticipantPsychologist_required()
def PsychologicalTest(request):
    registrations = Registrations.objects.all()
    
    if request.user.role == Users.PARTICIPANT:
        registrations = Registrations.objects.filter(User=request.user).order_by('TestSchedule__Date')
    elif request.user.role == Users.PSYCHOLOGIST:
        registrations = Registrations.objects.filter(TestSchedule__Psychologist=request.user).order_by('TestSchedule__Date', 'ParticipantNumber')

    serialized_data = [
        {
            'id': reg.id,
            'name': f"{reg.User.first_name} {reg.User.last_name}",
            'schedule_name': reg.TestSchedule.Name,
            'psychologist': f"{reg.TestSchedule.Psychologist.first_name} {reg.TestSchedule.Psychologist.last_name}",
            'number': reg.ParticipantNumber,
            'location': reg.TestSchedule.Location,
            'date': reg.TestSchedule.Date.isoformat(),
            'status': reg.Status
        }
        for reg in registrations
    ]

    return render(request, 'MindSphere/test.html', context={
        'section': 'psychological-test',
        'registrations_json': serialized_data
    })

@user_required()
def DeleteRegistration(request, pk):
    if request.method == 'DELETE':
        try:
            registration = Registrations.objects.get(id=pk)
            registration.delete()
            return JsonResponse({
                'status': 'success', 
                'message': 'Registration deleted successfully!'
            })
        except Registrations.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'Registrations not found.'
            })
        
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method.'
    })
 
@admin_required()
def PsycologistManagement(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = Users.PSYCHOLOGIST
            user.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Successfully created psychologist account!'
            })

        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list

            return JsonResponse({
                'status': 'error',
                'message': 'Failed creating account.',
                'errors': errors
            })
    return render(request, 'MindSphere/psychologist.html', context={'section' : 'psychologist'})

@login_required()
def History(request):
    return render(request, 'MindSphere/history.html', context={'section' : 'history'})

