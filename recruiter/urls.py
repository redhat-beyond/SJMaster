from django.urls import path
from recruiter.views import (CreateNewJobForm, recruiter_view_my_jobs_and_applications,
                             update_recruiter_account_settings_view)

urlpatterns = [
    path('recruiter/create_new_job_form/',
         CreateNewJobForm.as_view(), name='create_new_job_form'),
    path('myjobs', recruiter_view_my_jobs_and_applications, name='myjobs'),
    path('recruiter/account_settings/', update_recruiter_account_settings_view, name='recruiter_account_settings'),

]
