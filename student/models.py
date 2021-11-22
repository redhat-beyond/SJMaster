from django.db import models
from django.conf import settings


class EducationalInstitution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_institutions_with_enrolled_students(cls):
        """
        Return all institutions that have enrolled students as a QuerySet
        """
        return cls.objects.filter(students__isnull=False)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True)
    educational_institution = models.ForeignKey(EducationalInstitution, on_delete=models.PROTECT, default=None,
                                                related_name="students")
    graduation_date = models.DateField()

    def __str__(self):
        return f'{self.full_name}'

    @classmethod
    def get_students_enrolled_at(cls, institutions):
        """
        Gets all the students that are enrolled at one of the given institutions
        """
        return cls.objects.filter(educational_institution__in=institutions)

    @classmethod
    def get_students_graduate_after(cls, year):
        """
        Gets all the students from the DB that graduate after a given year
        """
        return cls.objects.filter(graduation_date__year__gte=year)
