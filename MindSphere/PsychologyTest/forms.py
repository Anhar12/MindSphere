from django import forms
from .models import Users, TestSchedules, Registrations, Results
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password confirmation does not match.")
        
        return cleaned_data
    
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = TestSchedules
        fields = ['Name', 'Psychologist', 'Description', 'Date', 'Location', 'Capacity', 'Image']
