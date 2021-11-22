from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView
from .models import Account, Profile
from .forms import AccountForm, RegisterForm, AccountUpdateForm, PasswordsChangingForm, UserProfileForm
from django.contrib.auth.hashers import make_password

class CreateUserProfileView(CreateView):
    model = Profile
    fields = ['bio', 'picture', 'facebook_url', 'twitter_url', 'instagram_url']
    template_name = 'registration/create_user_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user;
        print("Forming...")
        return super().form_valid(form);

    #def post(self, request):
    #    form = UserProfileForm(request.POST)
    #    if form.is_valid():
     #       profile = form.save(commit=False)
    #        #profile.user = request.user;
    #        profile.save();
    #        print("I am in post")
    #        return redirect(profile.get_absolute_url())

class UserProfileView(DetailView):
    model = Profile
    template_name = "registration/user_profile.html"

    def get_context_data(self,*args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        users = Profile.objects.all();
        profile = get_object_or_404(Profile, id = self.kwargs['pk'])
        context['profile'] = profile;

        return context

class EditUserProfileView(UpdateView):
    model = Profile
    template_name = "registration/edit_user_profile.html"
    fields = ['bio', 'picture', 'facebook_url', 'twitter_url', 'instagram_url']
    success_url = reverse_lazy('home')

class EditUserProfileSettingsView(UpdateView):
    model = Profile
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        users = Profile.objects.all();
        profile = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['profile'] = profile;

        return context

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

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'accs/acc_edit.html'
    success_url = reverse_lazy('about')

    def get_object(self):
        return self.request.user;

class UserRegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            print(reg_form)
            user = reg_form.save(commit=False)
            user.is_staff = False
            user.password = make_password(user.password)
            user.save()
            return redirect(self.get_success_url())

    def get_success_url(self):
        print("In success function")
        return self.success_url


class AccountChangePasswordView(PasswordChangeView):
    form_class = PasswordsChangingForm

    success_url = reverse_lazy('about')
    template_name = 'registration/password_change.html'

@method_decorator(csrf_exempt, name='dispatch')
class SaveJSONView(View):
    model = Profile
    fields = ['bio', 'picture', 'facebook_url', 'twitter_url', 'instagram_url']

    def get(self, request, pk):
        bla = {'bed':'breakfast'}
        return JsonResponse(bla);

    def post(self, request, pk):
        return JsonResponse({});