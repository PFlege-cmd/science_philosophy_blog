from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class UserCreateView(LoginRequiredMixin, View):
