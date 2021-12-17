from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recruiter, Company


class RecuiterRegistrationForm(UserCreationForm):
    queryset = Company.objects.all()
    name = forms.CharField(max_length=255)
    company = forms.ModelChoiceField(queryset)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)

    class Meta1:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RecuiterRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        user2 = Recruiter(user=user,
                          name=self.cleaned_data['name'],
                          company=self.cleaned_data['company'],
                          email=self.cleaned_data['email'],
                          phone_number=self.cleaned_data['phone_number'])
        user2.save()
        return user2
