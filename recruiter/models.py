from django.db import models
from django.conf import settings


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
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, related_name='recruiters')
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
