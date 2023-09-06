"""referral_system URL Configuration

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
from django.urls import path
from django.contrib.auth.decorators import login_required
from referral.views import ProfileView, ProfileAPIView
from account.views import (
    AuthorizationView, 
    LogoutView, 
    AuthorizationAPIView,
    LogoutAPIView
)

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path(
        "", 
        login_required(ProfileView.as_view()), 
        name="profile"
    ),
    path("login/", AuthorizationView.as_view(), name="login"),
        path(
        "logout/", 
        login_required(LogoutView.as_view()),
        name="logout"
    ),

    path(
        "api/v1/login/",
        AuthorizationAPIView.as_view(), 
        name="login_api"
    ),
    path("api/v1/logout/", LogoutAPIView.as_view(), name="logout_api"),
    path("api/v1/profile/", ProfileAPIView.as_view(), name="profile_api")
]
