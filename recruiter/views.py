# from django.shortcuts import render

# Create your views here.

from datetime import date
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView
from jobboard.models import Job
from recruiter.models import Recruiter


def job_created_successfully(request):
    return render(request, 'job_created_successfully.html')


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
