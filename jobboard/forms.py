from django import forms
from jobboard.models import Job


class CreateNewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'major', 'work_from', 'description', 'city', 'address', 'title_keywords']
