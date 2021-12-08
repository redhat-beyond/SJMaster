# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from recruiter.models import Recruiter


class UpdateRecruiterSettings(UserPassesTestMixin, UpdateView):
    model = Recruiter
    fields = ('name', 'company', 'email', 'phone_number')
    template_name = 'recruiter_account_settings.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])
