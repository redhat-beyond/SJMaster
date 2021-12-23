from django.urls import path
from jobboard.views import board, create_new_job_form, job_created_successfully, job_detail_view
from job_application.views import add_student_to_job_application


urlpatterns = [
    path('', board, name='board'),
    path('recruiter/create_new_job_form/', create_new_job_form, name='create_new_job_form'),
    path('job_created_successfully/', job_created_successfully, name='job_created'),
    path('job/<slug:id>/', job_detail_view),
    path('job/<slug:id>/apply_for_job/', add_student_to_job_application)
]
