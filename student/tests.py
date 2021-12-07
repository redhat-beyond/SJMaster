import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

from student.models import Student, EducationalInstitution, Major
from datetime import date


@pytest.fixture
def example_institution_a():
    institution = EducationalInstitution(name="A")
    institution.save()
    return institution


@pytest.fixture
def example_institution_b():
    institution = EducationalInstitution(name="B")
    institution.save()
    return institution


@pytest.fixture
def example_student_a(example_institution_a):
    example_user = User.objects.create_user("test", "testpassword")
    example_user.save()
    student = Student(user=example_user, full_name="test user", email="test@test.com", date_of_birth=date(2020, 7, 13),
                      phone_number="0000000000", educational_institution=example_institution_a, major=Major.UNDECIDED,
                      about="testing", graduation_date=date(2020, 7, 13))
    student.save()
    return student


@pytest.fixture
def example_student_b(example_institution_b):
    example_user = User.objects.create_user("test2", "testpassword")
    example_user.save()
    student = Student(user=example_user, full_name="test user2", email="test2@test.com",
                      date_of_birth=date(2023, 7, 13),
                      phone_number="0000000000", educational_institution=example_institution_b,
                      major=Major.COMPUTER_SCIENCE,
                      about="testing",
                      graduation_date=date(2023, 7, 13))
    student.save()
    return student


@pytest.mark.django_db
def test_get_institutions_with_enrolled_students_returns_institutions_with_enrolled_students_as_query_set(
        example_student_a, example_institution_a, example_institution_b):
    institution_query_set = EducationalInstitution.get_institutions_with_enrolled_students()
    assert isinstance(institution_query_set, QuerySet)
    assert all(isinstance(inst, EducationalInstitution) for inst in institution_query_set)
    assert list(institution_query_set.values_list("name")) == [(example_institution_a.name,)]


@pytest.mark.django_db
def test_get_students_enrolled_at_given_institutions_returns_students_enrolled_at_the_given_institutions_as_a_query_set(
        example_institution_a, example_institution_b, example_student_a, example_student_b):
    students_query_set = Student.get_students_enrolled_at_specified_institutions([example_institution_a])
    assert isinstance(students_query_set, QuerySet)
    assert all(isinstance(student, Student) for student in students_query_set)
    assert list(
        students_query_set.values_list("user", "full_name", "email", "date_of_birth", "phone_number",
                                       "educational_institution",
                                       "graduation_date")) == [
               (example_student_a.user.id, example_student_a.full_name, example_student_a.email,
                example_student_a.date_of_birth,
                example_student_a.phone_number,
                example_student_a.educational_institution.id, example_student_a.graduation_date), ]


@pytest.mark.django_db
def test_get_students_graduate_after_returns_students_that_graduate_after_the_given_year_as_query_set(
        example_student_a, example_student_b):
    students_grad_after_2023_query_set = Student.get_students_that_graduate_after_specified_year(2023)
    assert isinstance(students_grad_after_2023_query_set, QuerySet)
    assert all(isinstance(student, Student) for student in students_grad_after_2023_query_set)
    assert list(
        students_grad_after_2023_query_set.values_list("user", "full_name", "email", "date_of_birth", "phone_number",
                                                       "educational_institution",
                                                       "graduation_date")) == [
               (example_student_b.user.id, example_student_b.full_name, example_student_b.email,
                example_student_b.date_of_birth,
                example_student_b.phone_number,
                example_student_b.educational_institution.id, example_student_b.graduation_date)]


@pytest.mark.django_db
def test_if_user_is_a_student_returns_true_if_the_auth_user_is_associated_with_a_student_account(example_student_a):
    example_user_not_student = User.objects.create_user("notstudent", "password")
    example_user_not_student.save()
    assert Student.is_student(example_user_not_student.id) is False
    assert Student.is_student(example_student_a.user.id) is True
