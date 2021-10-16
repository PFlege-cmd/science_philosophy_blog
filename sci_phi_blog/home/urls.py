from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import MainView, AboutView;

urlpatterns = [
    path('', MainView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),
]
