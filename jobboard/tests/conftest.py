import pytest
from student.models import Major
from datetime import date
from django.contrib.auth.models import User
from student.models import Student, EducationalInstitution


@pytest.fixture
def example_institution_a():
    institution = EducationalInstitution(name="A")
    institution.save()
    return institution


@pytest.fixture
def example_student_a(example_institution_a):
    example_user = User.objects.create_user("test", "testpassword")
    example_user.save()
    student = Student(user=example_user, full_name="test user", email="test@test.com", date_of_birth=date(2020, 7, 13),
                      phone_number="0000000000", educational_institution=example_institution_a,
                      major=Major.COMPUTER_SCIENCE, about="testing", graduation_date=date(2020, 7, 13))
    student.save()
    return student
