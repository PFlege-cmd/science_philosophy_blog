from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import MainView;

urlpatterns = [
    path('', MainView.as_view(), name="home"),
]
