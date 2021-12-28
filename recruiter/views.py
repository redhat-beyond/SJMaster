from django.contrib import messages
from .forms import RecuiterRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from jobboard.models import Job
from recruiter.models import Recruiter
from job_application.models import Application
import jobboard.views
from .forms import UpdateRecruiterAccountSettingsForm


def recruiter_view_my_jobs_and_applications(request):
    context = {}
    recruiter_object = get_object_or_404(Recruiter, user_id=request.user.id)
    recruiter_jobs = Job.get_jobs_by_recruiter_id(recruiter_object)
    job_applications_dictionary = {}
    for job in recruiter_jobs:
        job_applications_dictionary[job] = list(
            Application.get_applications_by_job(job))
    context["jobs_and_applications"] = job_applications_dictionary
    jobboard.views.add_navbar_links_to_context(request, context)
    return render(request, "recruiter_my_jobs_and_applications.html", context)


def account_update_success(request):
    context = {}
    return render(request, 'account_settings_update_success.html', context)


def update_recruiter_account_settings_view(request):
    context = {}
    jobboard.views.add_navbar_links_to_context(request, context)
    recruiter_object = get_object_or_404(Recruiter, user_id=request.user.id)
    update_recruiter_form = UpdateRecruiterAccountSettingsForm(request.POST or None, instance=recruiter_object)
    context["form"] = update_recruiter_form
    if request.method == 'GET':
        return render(request, "recruiter_account_settings.html", context)

    elif request.method == "POST" and update_recruiter_form.is_valid():
        update_recruiter_form.save()
        return redirect("/account_update_success/", context)

    elif request.method == "POST" and not update_recruiter_form.is_valid():
        return render(request, "recruiter_account_settings.html", context)


def recruiterRegister(request):
    if request.method == 'POST':
        form = RecuiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Your account has been created. You can log in now!"
            messages.success(request, f'{message}')
            return redirect('/recruiter_created_successfully')
    else:
        form = RecuiterRegistrationForm()

    context = {'form': form}
    jobboard.views.add_navbar_links_to_context(request, context)
    return render(request, 'recruiter/registerRecruiter.html', context)


def recruiter_created_successfully(request):
    context = {}
    jobboard.views.add_navbar_links_to_context(request, context)
    return render(request, 'recruiter/recruiter_created_successfully.html', context)
