from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import UserCreateView

urlpatterns = [
    path('create_user', UserCreateView.as_view(), name="create_user"),
]
