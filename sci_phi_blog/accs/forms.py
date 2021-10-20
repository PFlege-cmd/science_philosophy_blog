from django import forms
from .models import Account


class UserForm(forms.ModelForm):
    class Meta:
        Model = Account
