from django.shortcuts import render, get_object_or_404, redirect

import jobboard
from .forms import CreateNewJobForm
from .models import Job
from datetime import date, timedelta
from student.models import Student
from recruiter.models import Recruiter
from job_application.models import Application


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
    add_navbar_links_to_context(request, content)
    return render(request, 'jobboard/board.html', content)


def add_navbar_links_to_context(request, context):
    if Student.is_student(request.user.id):
        context['navbar_links'] = {"Account Settings": "/student/account_settings/", "Logout": "/logout",
                                   f"Welcome {request.user.username}": "#"}

    elif Recruiter.is_recruiter(request.user.id):
        context['navbar_links'] = {"Account Settings": "/recruiter/account_settings/", "My Jobs": "/myjobs",
                                   "Create Job": "/recruiter/create_new_job_form", "Logout": "/logout",
                                   f"Welcome {request.user.username}": "#"}
    elif request.user.is_authenticated:
        context['navbar_links'] = {"Logout": "/logout"}
    else:
        context['navbar_links'] = {"Login": "/login"}


def create_new_job_form(request):
    recruiter_object = get_object_or_404(Recruiter, user_id=request.user.id)
    form = CreateNewJobForm()
    context = {}
    if request.method == 'POST':
        form = CreateNewJobForm(request.POST)
        if form.is_valid():
            form.instance.company = recruiter_object.company
            form.instance.recruiter = recruiter_object
            form.instance.date_created = date.today()
            form.save()
            return redirect("/job_created_successfully/", context)
    context = {'form': form}
    jobboard.views.add_navbar_links_to_context(request, context)
    return render(request, "create_new_job_form.html", context)


def job_created_successfully(request):
    return render(request, 'job_created_successfully.html')


def job_detail_view(request, id):
    context = dict()
    try:
        context["job_data"] = Job.objects.get(id=id)
        # add edit page for recruiter - context["recruiter_job_owner"] =...
    except Job.DoesNotExist:
        return render(request, "jobboard/no_such_job.html")

    context["is_student"] = Student.is_student(request.user.id)
    context["is_recruiter"] = Recruiter.is_recruiter(request.user.id)

    if context["is_student"]:
        context["is_student_applied"] = check_if_student_already_applied(Student.get_student(request.user),
                                                                         context["job_data"])
    return render(request, "jobboard/job.html", context)


def check_if_student_already_applied(student, job):
    applications_for_current_job = set(Application.get_applications_by_job(job))
    applications_for_current_student = set(Application.get_applications_by_student(student))
    return len(applications_for_current_job.intersection(applications_for_current_student)) > 0
