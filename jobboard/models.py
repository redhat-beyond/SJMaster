from django.db import models
from recruiter.models import Company
from student.models import Student


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class JobTitleKeyword(models.Model):
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=255, choices=[("Full-Time", "Full-Time"),
                                                         ("Part-Time", "Part-Time"),
                                                         ("Internship", "Internship")])
    work_from = models.CharField(max_length=255, choices=[("Office_Only", "Office_Only"),
                                                          ("Remote_Only", "Remote_Only"),
                                                          ("Hybrid", "Hybrid")], default="Office_Only")
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date_created = models.DateField()
    title_keywords = models.ManyToManyField(JobTitleKeyword)

    def __str__(self):
        return f"{self.title}, {self.company.name}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateField()

    def __str__(self):
        return f"{self.student.name} applied to {self.job}"
