from django import forms
from .models import Student


class UpdateStudentAccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "email", "date_of_birth", "phone_number", "educational_institution",
                  "major", "about", "graduation_date"]
