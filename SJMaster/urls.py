from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("student.urls"), name="student_urls"),
    path('', include("recruiter.urls"), name="recruiter_urls"),
    path('', include("login.urls"), name="login_urls"),
    path('', include("jobboard.urls"), name="jobboard_urls"),
]
