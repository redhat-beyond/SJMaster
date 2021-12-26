from django.urls import path
from jobboard.views import board, create_new_job_form, job_created_successfully

urlpatterns = [
    path('', board, name='board'),
    path('recruiter/create_new_job_form/', create_new_job_form, name='create_new_job_form'),
    path('job_created_successfully/', job_created_successfully, name='job_created')
]
