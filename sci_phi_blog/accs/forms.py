from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username','password', 'is_admin', 'is_staff']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username','password']
