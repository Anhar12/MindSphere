from django import forms
from .models import Users
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError(f"{password} do not match with {confirm_password}")
        return password
