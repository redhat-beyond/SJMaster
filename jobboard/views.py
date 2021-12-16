from django.shortcuts import render

from student.views import add_is_student_to_context
from .models import Job
from datetime import date, timedelta
from student.models import Student
from recruiter.models import Recruiter
from recruiter.views import add_is_recruiter_to_context


def get_content_if_user_is_student(request):
    """
    If the user is a student then the jobs that will automatically
    be displayed will be jobs that correspond to that student's degree
    """
    user_as_student = Student.get_student(request.user.id)
    jobs_by_student_major = Job.get_jobs_by_major(user_as_student.major)
    content = {'jobs_to_display': jobs_by_student_major,
               'user': request.user,
               'user_is_student': True,
               'user_is_recruiter': False,
               'user_as_student': user_as_student}
    return content


def get_content_if_user_is_not_student(request, user_is_recruiter):
    """
    If the user is not a student then the jobs that will automatically
    be displayed will be jobs that have been created in the past 6 months
    """
    date_six_months_ago = date.today() - timedelta(days=180)
    latest_jobs = Job.get_jobs_posted_on_or_after_specific_date(
        date_six_months_ago)
    content = {'jobs_to_display': latest_jobs,
               'user': request.user,
               'user_is_student': False,
               'user_is_recruiter': user_is_recruiter}
    if user_is_recruiter:
        content['user_as_recruiter'] = Recruiter.get_recruiter(request.user.id)
    return content


def board(request):
    user_is_student = Student.is_student(request.user.id)
    user_is_recruiter = Recruiter.is_recruiter(request.user.id)
    if user_is_student:
        content = get_content_if_user_is_student(request)
    else:
        content = get_content_if_user_is_not_student(request, user_is_recruiter)
    add_is_recruiter_to_context(request, content)
    add_is_student_to_context(request, content)
    return render(request, 'jobboard/board.html', content)
