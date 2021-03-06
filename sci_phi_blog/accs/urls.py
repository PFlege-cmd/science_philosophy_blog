from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import UserCreateView, UserRegisterView, UserChangeView, AccountChangePasswordView, UserProfileView, \
    EditUserProfileView, EditUserProfileSettingsView, CreateUserProfileView, SaveJSONView

urlpatterns = [
    path('create_user', UserCreateView.as_view(), name="create_user"),
    path('register', UserRegisterView.as_view(), name='register'),
    path('edit', UserChangeView.as_view(), name="edit_user"),
    path('create/profile', CreateUserProfileView.as_view(), name='create_profile'),
    path('<int:pk>/profile', UserProfileView.as_view(), name="profile_page"),
    path('<int:pk>/profile/edit_profile', EditUserProfileView.as_view(), name="edit_profile_page"),
    path('<int:pk>/profile/save', SaveJSONView.as_view(), name="save_json"),
    path('profile_settings', EditUserProfileSettingsView.as_view(), name="edit_profile"),
]
