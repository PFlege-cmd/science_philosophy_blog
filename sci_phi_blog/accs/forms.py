import urllib.parse
from urllib import parse
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import Account, Profile


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

        widgets = {
            'old_password': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password1': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password2': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserProfileForm(forms.ModelForm):



    class Meta:
        model = Profile
        fields = ['bio', 'picture', 'facebook_url', 'twitter_url', 'instagram_url']

        widgets = {
            'bio' : forms.Textarea(attrs={'class': 'form-control'}),
            'facebook_url' : forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url' : forms.TextInput(attrs={'class':'form-control'}),
            'instagram_url' : forms.TextInput(attrs={'class': 'form-control'})
        }
    def clean_facebook_url(self):
        fb_url = self.cleaned_data['facebook_url']
        return check_if_url_exists_then_form(fb_url)

    def clean_twitter_url(self):
        tw_url = self.cleaned_data['twitter_url']
        print("Check twitter")

        return check_if_url_exists_then_form(tw_url)

    def clean_instagram_url(self):
        in_url = self.cleaned_data['instagram_url']
        print("Check insta")
        return check_if_url_exists_then_form(in_url)

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) > 1000:
            raise ValidationError("Description is too long. Limit yourself to 1000 characters")
        return bio;

    def clean(self):
        data = self.cleaned_data
        print('Check all');

def check_if_url_exists_then_form(url:str) -> str:
    print("In sub")
    if not url:
        return url
    else:
        # print("Check facebook")
        return check_url(url)

def check_url(url:str) -> str:
    parsed_url = parse.urlparse(url)
    print("Uses sub-method")

    if parsed_url.netloc and parsed_url.scheme:
        print("Network location is: " + str(parsed_url.netloc))
        print("Scheme is:" + str(parsed_url.scheme))
        return url
    else:
        raise ValidationError("Provide valid url")


