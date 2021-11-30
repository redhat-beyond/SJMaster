from django.db import models
from recruiter.models import Company, Recruiter
import datetime


class Region(models.Model):
    name = models.CharField(max_length=255)

    def _str_(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def _str_(self):
        return self.name


class JobTitleKeyword(models.Model):
    keyword = models.CharField(max_length=255)

    def _str_(self):
        return self.keyword


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.PROTECT, default=None)
    job_type = models.CharField(max_length=255, choices=[("Full-Time", "Full-Time"),
                                                         ("Part-Time",
                                                          "Part-Time"),
                                                         ("Internship", "Internship")])
    work_from = models.CharField(max_length=255, choices=[("Office-Only", "Office-Only"),
                                                          ("Remote-Only",
                                                           "Remote-Only"),
                                                          ("Hybrid", "Hybrid")], default="Office_Only")
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date_created = models.DateField()
    title_keywords = models.ManyToManyField(JobTitleKeyword)

    @classmethod
    def get_jobs_by_city_name(cls, city_name):
        """
        Allows students to search for a job based on the city it is located in
        """
        return set(cls.objects.filter(city=City.objects.get(name=city_name)))

    @classmethod
    def get_jobs_by_region_name(cls, region_name):
        """
        Allows students to search for a job based on the region it is located in
        """
        jobs_to_return = set()
        region = Region.objects.get(name=region_name)
        for city in City.objects.filter(region=region):
            jobs_to_return.update(cls.get_jobs_by_city_name(city.name))
        return jobs_to_return

    @classmethod
    def get_jobs_by_job_type(cls, job_type):
        """
        Allows students to search for a job based on the job-type (full-time, internship or part-time)
        """
        return set(cls.objects.filter(job_type=job_type))

    @classmethod
    def get_jobs_by_keywords(cls, *keywords_as_string):
        """
        Allows students to search for a job based on one ore more keywords linked to the job
        """
        jobs_to_return = set()
        for keyword in keywords_as_string:
            keyword_object = JobTitleKeyword.objects.get(keyword=keyword)
            jobs_to_return.update(
                set(cls.objects.filter(title_keywords=keyword_object)))
        return jobs_to_return

    @classmethod
    def get_jobs_posted_on_or_after_specific_date(cls, date):
        """
        Allows students to search for a job that was posted on or after a specific date
        """
        return set(cls.objects.filter(date_created__range=[date, datetime.date.today()]))

    @classmethod
    def get_jobs_by_work_model(cls, work_model):
        """
        Allows students to search for a job based on the work model (Office-Only, Remote-Only or Hybrid)
        """
        return set(cls.objects.filter(work_from=work_model))

    @classmethod
    def get_jobs_by_company_name(cls, company_name):
        """
        Allows students to search for a job based on the company
        """
        return set(cls.objects.filter(company=Company.objects.get(name=company_name)))

    def _str_(self):
        return f"{self.title}, {self.company.name}"
