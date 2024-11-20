from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('contact', views.Contact, name='contact'),
    path('sign-in', views.SignIn, name='sign-in'),
    path('sign-up', views.SignUp, name='sign-up'),
    path('sign-out', views.SignOut, name='sign-out'),
    path('mind-sphere/dashboard', views.Dashboard, name='dashboard'),
    
    path('mind-sphere/test-schedule', views.TestSchedule, name='test-schedule'),
    path('mind-sphere/add-schedule', views.AddSchedule, name='add-schedule'),
    path('mind-sphere/update-schedule/<int:pk>', views.UpdateSchedule, name='update-schedule'),
    path('mind-sphere/delete-schedule/<int:pk>', views.DeleteSchedule, name='delete-schedule'),
    
    path('mind-sphere/psychological-test', views.PsychologicalTest, name='psychological-test'),
    path('mind-sphere/psychologist', views.PsycologistManagement, name='psychologist'),
    path('mind-sphere/history', views.History, name='history'),
    
]
