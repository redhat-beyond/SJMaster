import pytest
from pytest_django.asserts import assertTemplateUsed
from jobboard.models import Job
from datetime import date, timedelta
from django.contrib.auth.models import User
from recruiter.models import Recruiter

# The tests use the data that is already in the db from the migration files


@pytest.mark.django_db
def test_page_display_to_user_that_is_not_student_and_not_recruiter(client):
    example_user = User.objects.create_user("username", "password")
    client.force_login(example_user)
    response = client.get("/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context['user'] == example_user
    assert response.context['user_is_student'] is False
    assert response.context['user_is_recruiter'] is False
    date_six_months_ago = date.today() - timedelta(days=180)
    jobs_to_display = Job.get_jobs_posted_on_or_after_specific_date(date_six_months_ago)
    # test that jobs displayed are only jobs created 6 months ago
    assert response.context['jobs_to_display'] == jobs_to_display


@pytest.mark.django_db
def test_page_display_to_user_that_is_student(client, example_student_a):
    client.force_login(example_student_a.user)
    response = client.get("/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context['user'] == example_student_a.user
    assert response.context['user_is_student'] is True
    assert response.context['user_is_recruiter'] is False
    assert response.context['user_as_student'] == example_student_a
    jobs_by_student_major = Job.get_jobs_by_major(example_student_a.major)
    # test that jobs displayed are only jobs corresponding to the student's major
    assert response.context['jobs_to_display'] == jobs_by_student_major


@pytest.mark.django_db
def test_page_display_to_user_that_is_recruiter(client):
    example_recruiter_a_from_db = Recruiter.objects.get(name='a')
    client.force_login(example_recruiter_a_from_db.user)
    response = client.get("/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context['user'] == example_recruiter_a_from_db.user
    assert response.context['user_is_student'] is False
    assert response.context['user_is_recruiter'] is True
    assert response.context['user_as_recruiter'] == example_recruiter_a_from_db
    date_six_months_ago = date.today() - timedelta(days=180)
    jobs_to_display = Job.get_jobs_posted_on_or_after_specific_date(date_six_months_ago)
    # test that jobs displayed are only jobs created 6 months ago
    assert response.context['jobs_to_display'] == jobs_to_display
