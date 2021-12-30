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
               'jobs_intro_message': 'Here are some jobs that match your profile',
               'user': request.user,
               'user_is_student': True,
               'user_is_recruiter': False,
               'user_as_student': user_as_student,
               'user_name': f"{request.user.first_name} {request.user.last_name}"}
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
               'jobs_intro_message': 'Here are jobs created in the last 6 months',
               'user': request.user,
               'user_is_student': False,
               'user_is_recruiter': user_is_recruiter}
    if user_is_recruiter:
        content['user_as_recruiter'] = Recruiter.get_recruiter(request.user.id)
        content['user_name'] = f"{request.user.first_name} {request.user.last_name}"
    return content


def searched_by_company_or_keyword(searched_name):
    jobs_by_company = Job.get_jobs_by_company_name(searched_name)
    jobs_by_keyword = Job.get_jobs_by_keyword(searched_name)
    return jobs_by_company.union(jobs_by_keyword)


def searched_by_city(searched_city):
    jobs_by_city = Job.get_jobs_by_city_name(searched_city)
    return jobs_by_city


def board(request):
    user_is_student = Student.is_student(request.user.id)
    user_is_recruiter = Recruiter.is_recruiter(request.user.id)
    if user_is_student:
        content = get_content_if_user_is_student(request)
    else:
        content = get_content_if_user_is_not_student(request, user_is_recruiter)

    # user hit the search button
    if request.method == "POST":
        searched_name = request.POST.get('searched_name')
        searched_city = request.POST.get('searched_city')
        content["searched_name"] = searched_name
        content["searched_city"] = searched_city
        if searched_name and not searched_city:
            content['jobs_to_display'] = searched_by_company_or_keyword(searched_name)
            content['jobs_intro_message'] = f"Here are jobs for '{searched_name}'"
        elif searched_city and not searched_name:
            content['jobs_to_display'] = searched_by_city(searched_city)
            content['jobs_intro_message'] = f"Here are jobs located at '{searched_city}"
        else:
            content['jobs_to_display'] = searched_by_city(searched_city).\
                intersection(searched_by_company_or_keyword(searched_name))
            content['jobs_intro_message'] = f"Here are jobs for '{searched_name}' located at '{searched_city}"
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
    except Job.DoesNotExist:
        return render(request, "jobboard/no_such_job.html")

    # setting a null default value if the user isn't recruiter or student
    user_indicator_template = None

    if Student.is_student(request.user.id):
        if check_if_student_already_applied(Student.get_student(request.user), context["job_data"]):
            user_indicator_template = "jobboard/student_user_applied_indicator.html"
        else:
            user_indicator_template = "jobboard/student_user_not_applied_indicator.html"

    elif Recruiter.is_recruiter(request.user.id):
        if context["job_data"].recruiter.user.id == request.user.id:
            user_indicator_template = "jobboard/recruiter_user_owns_job_indicator.html"

    context["user_indicator_template"] = user_indicator_template
    add_navbar_links_to_context(request, context)
    return render(request, "jobboard/job.html", context)


def check_if_student_already_applied(student, job):
    applications_for_current_job = set(Application.get_applications_by_job(job))
    applications_for_current_student = set(Application.get_applications_by_student(student))
    return len(applications_for_current_job.intersection(applications_for_current_student)) > 0
