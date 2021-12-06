import pytest
import datetime
from jobboard.models import Job
from django.db.models import QuerySet
from django.contrib.auth.models import User
from job_application.models import Application
from student.models import Student, EducationalInstitution


# The tests use the data that is already in the db from the migration files
@pytest.fixture
def example_institution():
    test_institution = EducationalInstitution(name="test_institution")
    test_institution.save()
    return test_institution


@pytest.fixture
def example_student(example_institution):
    test_user = User.objects.create_user("test", "testpassword")
    test_user.save()
    test_student = Student(user=test_user, full_name="test user", email="test_user@test.com",
                           date_of_birth=datetime.date(2020, 7, 13),
                           phone_number="0000000000", educational_institution=example_institution,
                           graduation_date=datetime.date(2020, 7, 13))
    test_student.save()
    return test_student


@pytest.fixture
def example_job_application(example_student):
    job_a = Job.objects.get(title="job_a")
    application_a = Application(
        job=job_a, student=example_student, date_applied=datetime.date(2021, 7, 15))
    application_a.save()
    return application_a


@pytest.mark.django_db
def test_get_all_applications_by_a_specified_job_returns_all_applications_as_a_query_set(
        example_job_application, example_student):
    job_a = Job.objects.get(title="job_a")
    temp_applications_1 = Application.get_applications_by_job(job_a)
    assert isinstance(temp_applications_1, QuerySet)
    assert all(isinstance(application, Application)
               for application in temp_applications_1)
    assert list(temp_applications_1.values_list("job", "student", "date_applied")) == [
        (job_a.id, example_student.user.id, datetime.date(2021, 7, 15))]


@pytest.mark.django_db
def test_get_all_applications_by_a_specified_student_returns_all_applications_as_a_query_set(
        example_job_application, example_student):
    job_a = Job.objects.get(title="job_a")
    temp_applications_2 = Application.get_applications_by_student(
        example_student)
    assert isinstance(temp_applications_2, QuerySet)
    assert all(isinstance(application, Application)
               for application in temp_applications_2)
    assert list(temp_applications_2.values_list("job", "student", "date_applied")) == [
        (job_a.id, example_student.user.id, datetime.date(2021, 7, 15))]
