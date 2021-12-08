from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    website_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_all_recruiters_of_a_specified_company(self):
        """
        returns all recruiters of a specified company
        Input: a company instance
        Output: all recruiters of the company
        """
        return self.recruiters.all()

    @classmethod
    def get_all_companies(cls):
        """
        returns all existing companies in the website
        """
        return cls.objects.order_by("name")


class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, related_name='recruiters')
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def is_recruiter(cls, auth_user_id):
        """
        For checking if a currently logged in user is a Recruiter
        """
        return cls.objects.filter(user_id=auth_user_id).exists()
