from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .models import Account
from .forms import AccountForm, RegisterForm
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

class UserRegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    #def form_valid(self, form):
        #form.password = make_password(form.password)
    #    user = form.save(commit=False)
    #    user.password = make_password(user.password)
    #    form = RegisterForm(instance=user)
    #    super(UserRegisterView, self).form_valid(form)

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            print(reg_form)
            user = reg_form.save(commit=False)
            user.is_staff = False
            user.password = make_password(user.password)
            user.save()
            return redirect(self.success_url)

    #    else:
    #        return HttpResponse("Invalid")
