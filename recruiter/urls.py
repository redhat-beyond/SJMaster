from django.urls import path
from recruiter.views import (UpdateRecruiterSettings, CreateNewJobForm, recruiter_view_my_jobs_and_applications, )

urlpatterns = [
    path('recruiter/account_settings/<slug:pk>',
         UpdateRecruiterSettings.as_view(), name='recruiter_account_settings'),
    path('recruiter/create_new_job_form/',
         CreateNewJobForm.as_view(), name='create_new_job_form'),
    path('myjobs', recruiter_view_my_jobs_and_applications, name='myjobs'),
]
