from django.urls import path
from recruiter.views import (recruiter_view_my_jobs_and_applications,
                             update_recruiter_account_settings_view)

urlpatterns = [
    path('myjobs', recruiter_view_my_jobs_and_applications, name='myjobs'),
    path('recruiter/account_settings/', update_recruiter_account_settings_view, name='recruiter_account_settings'),
]
