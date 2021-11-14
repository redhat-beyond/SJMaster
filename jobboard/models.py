from django.db import models
from django.conf import settings


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    UNSPECIFIED = "U", "Unspecified"


class EducationalInstitutes(models.Model):
    institute_name = models.CharField(max_length=255)

    def __str__(self):
        return self.institute_name


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(max_length=500)
    company_website_url = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_id = models.ForeignKey(Company, on_delete=models.RESTRICT, related_name='recruiters')
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    educational_institute_name = models.ManyToManyField(EducationalInstitutes, related_name='students')
    graduation_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
