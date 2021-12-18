from datetime import datetime
from django.shortcuts import render, get_object_or_404
from jobboard.models import Job
from jobboard.views import check_if_student_already_applied
from .models import Application
from student.models import Student


def apply_success(request):
    return render(request, 'apply_success.html')


def add_student_to_job_application(request, id):
    student_object = get_object_or_404(Student, user_id=request.user.id)
    job = Job.objects.get(id=id)
    # if a student is trying to enter the url of applying to a job manually, while this student already applied
    if check_if_student_already_applied(student_object, job):
        return render(request, 'you_have_already_applied.html')
    Application(job=job, student=student_object, date_applied=datetime.today()).save()
    return render(request, 'apply_success.html')
