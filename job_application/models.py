from django.db import models
from student.models import Student
from jobboard.models import Job


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='application_job')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='application_student')
    date_applied = models.DateField()

    @classmethod
    def get_applications_by_job(cls, job):
        """
        Allows recuriters to search for all of the applications for some job.
        """
        return cls.objects.filter(job_id=job.id)

    @classmethod
    def get_applications_by_student(cls, student):
        """
        Allows students to search for all of their job applications.
        """
        return cls.objects.filter(student__user_id=student.user.id)

    def __str__(self):
        return f"{self.student.full_name} applied to {self.job}"
