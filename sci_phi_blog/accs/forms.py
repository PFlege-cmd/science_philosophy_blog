from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username','password', 'is_admin', 'is_staff']

        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username','password']

        widgets = {
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'password' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['email', 'username']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class' : 'form-control'}),
        }

class PasswordsChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length = 100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length= 100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta:
        model = Account
        fields = ['old_password', 'new_password1', 'new_password2']


