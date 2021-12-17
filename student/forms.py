from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, EducationalInstitution, Major


class UpdateStudentAccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "email", "date_of_birth", "phone_number", "educational_institution",
                  "major", "about", "graduation_date"]


class StudentRegistrationForm(UserCreationForm):
    educationalInstitution_Queryset = EducationalInstitution.objects.all()
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField()
    phone_number = forms.CharField(max_length=15)
    educational_institution = forms.ModelChoiceField(
        educationalInstitution_Queryset)
    major = forms.TypedChoiceField(choices=Major.choices)
    about = forms.CharField(widget=forms.Textarea)
    graduation_date = forms.DateField()

    class Meta1:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        user2 = Student(user=user,
                        full_name=self.cleaned_data['full_name'],
                        date_of_birth=self.cleaned_data['date_of_birth'],
                        phone_number=self.cleaned_data['phone_number'],
                        educational_institution=self.cleaned_data['educational_institution'],
                        major=self.cleaned_data['major'],
                        about=self.cleaned_data['about'],
                        graduation_date=self.cleaned_data['graduation_date'])
        user2.save()
        return user2
