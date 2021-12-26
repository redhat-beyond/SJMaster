import pytest
import jobboard
import student
from recruiter.models import Recruiter, Company
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


@pytest.fixture
def example_recruiter():
    example_user = User.objects.create_user("test", "testpassword")
    example_user.save()
    recruiter = Recruiter(user=example_user, name="test_recruiter",
                          company=Company.objects.get(name="example_company_a"), email="test@email",
                          phone_number="test_phone")
    recruiter.save()
    return recruiter


@pytest.fixture
def example_job_data_as_dictionary():
    example_job = {"title": 'example_job',
                   "major": student.models.Major.COMPUTER_SCIENCE,
                   "job_type": 'Full-Time',
                   "work_from": 'Office-Only',
                   "description": 'Junior software engineer',
                   "city": jobboard.models.City.objects.get(name="Tel Aviv-Yafo").id,
                   "address": 'Hashalom',
                   "title_keywords": [jobboard.models.JobTitleKeyword.objects.get(keyword="software").id]}
    return example_job
