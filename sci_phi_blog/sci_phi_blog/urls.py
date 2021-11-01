"""sci_phi_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

from accs.views import AccountChangePasswordView

app_name = "home"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('user/', include('accs.urls')),
    path('articles/', include('arts.urls')),
    path('user/profile/', views.profile_redirect, name='profile_redirect'),
    path('password/', AccountChangePasswordView.as_view(), name="password"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
