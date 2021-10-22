from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .models import Account
from .forms import AccountForm
from django.contrib.auth.hashers import make_password


class UserCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['email', 'username','password', 'is_admin', 'is_staff']
    template_name = "accs/acc_form.html"

    def post(self, request):


        acc_form = AccountForm(request.POST)
        if acc_form.is_valid():
            print(acc_form)
            user = acc_form.save(commit=False)
            user.is_staff = True
            user.password = make_password(user.password)
            user.save()
            return redirect(reverse("home"))

        else:
            return HttpResponse("Invalid input")


