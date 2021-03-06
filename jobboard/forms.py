from django import forms
from jobboard.models import Job


class FormControl(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form_field in self.visible_fields():
            form_field.field.widget.attrs['class'] = 'form-control'


class CreateNewJobForm(FormControl):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'major', 'work_from', 'description', 'city', 'address', 'title_keywords']
        widgets = {'description': forms.Textarea(attrs={'rows': '5'}), }
