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
from student.views import update_student_account_settings_view, account_update_success
from recruiter.views import (UpdateRecruiterSettings,
                             CreateNewJobForm,
                             job_created_successfully,
                             recruiterRegister,
                             recruiter_created_successfully,
                             recruiter_view_my_jobs_and_applications,)
from student.views import studentRegister, student_created_successfully


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', board, name='board'),
    path('', include("django.contrib.auth.urls"), name="login"),
    path('recruiter/account_settings/<slug:pk>',
         UpdateRecruiterSettings.as_view(), name='recruiter_account_settings'),
    path('recruiter/create_new_job_form/',
         CreateNewJobForm.as_view(), name='create_new_job_form'),
    path('job_created_successfully/',
         job_created_successfully, name='job_created'),
    path('myjobs', recruiter_view_my_jobs_and_applications, name='myjobs'),
    path('recruiter/account_settings/<slug:pk>',
         UpdateRecruiterSettings.as_view(), name='recruiter_account_settings'),
    path('student/account_settings/', update_student_account_settings_view,
         name="student_account_settings"),
    path('account_update_success/', account_update_success,
         name="account_update_success"),
    path('recruiter/account_settings/<slug:pk>',
         UpdateRecruiterSettings.as_view(), name='recruiter_account_settings'),
    path('student/account_settings/', update_student_account_settings_view,
         name="student_account_settings"),
    path('account_update_success/', account_update_success,
         name="account_update_success"),
    path('registerStudent/', studentRegister, name='registerStudent'),
    path('recruiterRegister/', recruiterRegister, name='recruiterRegister'),
    path('recruiter_created_successfully/', recruiter_created_successfully,
         name='recruiter_created_successfully'),
    path('student_created_successfully/', student_created_successfully,
         name='student_created_successfully')

]
