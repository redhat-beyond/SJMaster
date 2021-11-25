from django.db import models
from student.models import Student
from jobboard.models import Job


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='application_job')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='application_student')
    date_applied = models.DateField()

    def __str__(self):
        return f"{self.student.name} applied to {self.job}"
