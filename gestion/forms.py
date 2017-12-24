from django.contrib.auth.models import User
from django import forms

from .models import Companie, Employee

class CompanieForm(forms.ModelForm):

    class Meta:
        model = Companie
        fields = ['companie_name', 'address', 'companie_logo']

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_surname']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


