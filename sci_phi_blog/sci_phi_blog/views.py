from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def profile_redirect(request):
    return HttpResponseRedirect(reverse_lazy("home"));