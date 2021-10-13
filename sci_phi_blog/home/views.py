from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name = "home\\main.html";