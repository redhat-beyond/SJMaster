from django.urls import path
from recruiter.views import (
    update_recruiter_account_settings_view,
    recruiter_view_my_jobs_and_applications,
    company_created_successfully,
    companyRegister)

urlpatterns = [
    path('myjobs', recruiter_view_my_jobs_and_applications, name='myjobs'),
    path('recruiter/account_settings/', update_recruiter_account_settings_view, name='recruiter_account_settings'),
    path('companyRegister/', companyRegister, name='companyRegister'),
    path('company_created_successfully/', company_created_successfully, name='company_created_successfully'),
]
