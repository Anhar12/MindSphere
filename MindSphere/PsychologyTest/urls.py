from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('contact', views.Contact, name='contact'),
    path('sign-in', views.SignIn, name='sign-in'),
    path('sign-up', views.SignUp, name='sign-up'),
    path('sign-out', views.SignOut, name='sign-out'),
]
