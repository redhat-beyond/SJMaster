from django.db import models
from django.conf import settings


class EducationalInstitution(models.Model):
    institution_name = models.CharField(max_length=255)

    def __str__(self):
        return self.institution_name


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True)
    educational_institution_name = models.ManyToManyField(EducationalInstitution, related_name='students')
    graduation_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
