from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from jobboard.models import Job
from datetime import date
# from .forms import JobForm

from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from student.models import Student


def board(request):
    latest_jobs = Job.get_jobs_posted_on_or_after_specific_date(date(2021, 3, 1))
    return render(request, 'jobboard/board.html', {'latest_jobs': latest_jobs})


# def job(request):
#     job_by_id = Job.objects.get(request.job.id)
#     return render(request, 'jobboard/job.html', {"job_instance": job_by_id})


# after updating it will redirect to detail_View
def job_detail_view(request, id):
    # dictionary for initial data with job's field names as keys
    context = dict()
    is_student = Student.is_student(request.user.id)
    # add the dictionary during initialization
    try:
        context["data"] = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return render(request, "jobboard/no_such_job.html")
    add_is_student_to_context(request, context)
    return render(request, "jobboard/job.html", context)


def add_is_student_to_context(request, context):
    context["is_student"] = Student.is_student(request.user.id)

#
# def job_view(request):
#     context = {}
#
#     # create object of form
#     job_form_object = JobForm(request.GET or None, request.FILES or None)
#
#     # check if form data is valid
#     if job_form_object.is_valid():
#         # save the form data to model
#         job_form_object.save()
#
#     context['form'] = job_form_object
#     return render(request, "job.html", context)
