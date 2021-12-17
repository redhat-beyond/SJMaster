# from django.shortcuts import render

# Create your views here.

from datetime import date
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView
from jobboard.models import Job
from recruiter.models import Recruiter
from job_application.models import Application


def job_created_successfully(request):
    return render(request, 'job_created_successfully.html')


def recruiter_view_my_jobs_and_applications(request):
    context = {}
    try:
        recruiter_object = Recruiter.objects.get(user_id=request.user.id)
    except Recruiter.DoesNotExist:
        return render(request, "dead_end.html")
    recruiter_jobs = Job.get_jobs_by_recruiter_id(recruiter_object)
    job_applications_dictionary = {}
    for job in recruiter_jobs:
        job_applications_dictionary[job] = list(Application.get_applications_by_job(job))
    context["jobs_and_applications"] = job_applications_dictionary
    return render(request, "recruiter_my_jobs_and_applications.html", context)


class UpdateRecruiterSettings(UserPassesTestMixin, UpdateView):
    model = Recruiter
    fields = ('name', 'company', 'email', 'phone_number')
    template_name = 'recruiter_account_settings.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])


class CreateNewJobForm(CreateView, UserPassesTestMixin):
    model = Job
    fields = (
        'title', 'job_type', 'work_from', 'description', 'city', 'address', 'title_keywords')
    template_name = 'create_new_job_form.html'
    success_url = '/job_created_successfully'

    def test_func(self):
        return Recruiter.is_recruiter(self.request.user.id)

    def form_valid(self, form):
        logged_recruiter = Recruiter.objects.get(user_id=self.request.user.id)
        form.instance.recruiter = logged_recruiter
        form.instance.company = logged_recruiter.company
        form.instance.date_created = date.today()
        return super(CreateNewJobForm, self).form_valid(form)
