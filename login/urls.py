from django.urls import path, include
from recruiter.views import (recruiterRegister, recruiter_created_successfully, )
from student.views import studentRegister, student_created_successfully

urlpatterns = [
    path('', include("django.contrib.auth.urls"), name="login"),
    path('registerStudent/', studentRegister, name='registerStudent'),
    path('recruiterRegister/', recruiterRegister, name='recruiterRegister'),
    path('recruiter_created_successfully/', recruiter_created_successfully,
         name='recruiter_created_successfully'),
    path('student_created_successfully/', student_created_successfully,
         name='student_created_successfully')
]
