from django.db import models
from django.conf import settings


class EducationalInstitution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def get_institutions_with_enrolled_students(cls):
        """
        For recruiters to use, so they can know which institutions are relevant to choose students from.
        """
        return cls.objects.filter(students__isnull=False)


class Major(models.TextChoices):
    UNDECIDED = "U", "Undecided"
    COMPUTER_SCIENCE = "CS", "Computer Science"
    SOFTWARE_ENGINEER = "SWE", "Software Engineer"
    ELECTRICAL_ENGINEER = "EE", "Electrical Engineer"
    MECHANICAL_ENGINEER = "ME", "Mechanical Engineer"
    CIVIL_ENGINEER = "CE", "Civil Engineer"
    CHEMICAL_ENGINEER = "CHE", "Chemical Engineer"
    FINANCE = "FI", "Finance"
    HUMAN_RESOURCES = "HR", "Human Resources"
    COMMUNICATIONS = "COM", "Communications"
    LAW = "LAW", "Law"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True)
    educational_institution = models.ForeignKey(EducationalInstitution, on_delete=models.PROTECT, default=None,
                                                related_name="students")
    major = models.CharField(max_length=3, choices=Major.choices, default=Major.UNDECIDED)
    about = models.TextField(blank=True)
    graduation_date = models.DateField()

    def __str__(self):
        return f'{self.full_name}'

    @classmethod
    def get_students_enrolled_at_specified_institutions(cls, institutions):
        """
        For recruiters to use when they want to only view students from specific institutions.
        """
        return cls.objects.filter(educational_institution__in=institutions)

    @classmethod
    def get_students_that_graduate_after_specified_year(cls, year):
        """
        For recruiters to use when they want to view students according to their graduation year.
        """
        return cls.objects.filter(graduation_date__year__gte=year)
