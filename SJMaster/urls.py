"""SJMaster URL Configuration

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
from jobboard.views import board
from login.views import register_request
from recruiter.views import UpdateRecruiterSettings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', board, name='board'),
    path("register/", register_request, name="register"),
    path('', include("django.contrib.auth.urls"), name="login"),
    path('recruiter/account_settings/<slug:pk>', UpdateRecruiterSettings.as_view(),
         name='recruiter_account_settings')
]
