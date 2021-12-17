from datetime import datetime
from django.shortcuts import render, get_object_or_404
from jobboard.models import Job
from .models import Application
from student.models import Student


def apply_success(request):
    return render(request, 'apply_success.html')


def add_student_to_job_application(request, id):
    student_object = get_object_or_404(Student, user_id=request.user.id)
    Application(job=Job.objects.get(id=id), student=student_object, date_applied=datetime.date.today()).save()
    return render(request, 'apply_success.html')
