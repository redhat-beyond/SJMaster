import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed

from jobboard.models import Job
from recruiter.models import Recruiter


@pytest.mark.django_db
def test_job_display_to_user_that_is_student_not_applied(client, example_student_a):
    client.force_login(example_student_a.user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['is_student'] is True
    assert response.context['is_recruiter'] is False
    # example_student_a haven't applied to job with id=1
    assert response.context["is_student_applied"] is False
    job_to_display = Job.objects.get(id=1)
    assert response.context['job_data'] == job_to_display


@pytest.mark.django_db
def test_job_display_to_user_that_is_student_have_applied(client, example_student_a):
    client.force_login(example_student_a.user)
    # make student apply for job before checking the job read-more page
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    # checking how the job.html renders after applying
    response = client.get("/job/1/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['is_student'] is True
    assert response.context['is_recruiter'] is False
    # example_student_a haven't applied to job with id=1
    assert response.context["is_student_applied"] is True


@pytest.mark.django_db
def test_student_trying_to_apply_and_test_after_apply(client, example_student_a):
    client.force_login(example_student_a.user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['is_student'] is True
    assert response.context['is_recruiter'] is False
    # example_student_a haven't applied to job with id=1
    assert response.context["is_student_applied"] is False
    # example_student_a haven't applied to job with id=1 yet
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    # checking if apply_success was rendered
    assertTemplateUsed(response, 'apply_success.html')


@pytest.mark.django_db
def test_student_tries_to_manually_applying_for_job_again(client, example_student_a):
    client.force_login(example_student_a.user)
    # example_student_a haven't applied to job with id=1 yet
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    # checking if apply_success was rendered
    assertTemplateUsed(response, 'apply_success.html')
    # trying to apply again
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'you_have_already_applied.html')


@pytest.mark.django_db
def test_job_display_to_user_that_is_recruiter(client):
    example_recruiter_a_from_db = Recruiter.objects.get(name='a')
    client.force_login(example_recruiter_a_from_db.user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['is_student'] is False
    assert response.context['is_recruiter'] is True
    job_to_display = Job.objects.get(id=1)
    assert response.context['job_data'] == job_to_display


@pytest.mark.django_db
def test_job_display_to_user_that_is_not_student_and_not_recruiter(client):
    example_user = User.objects.create_user("username", "password")
    client.force_login(example_user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['is_student'] is False
    assert response.context['is_recruiter'] is False
    job_to_display = Job.objects.get(id=1)
    assert response.context['job_data'] == job_to_display


@pytest.mark.django_db
def test_try_displaying_non_exist_job_user_is_student(client, example_student_a):
    client.force_login(example_student_a.user)
    # job with id=8 does not exist
    response = client.get("/job/8/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/no_such_job.html')


@pytest.mark.django_db
def test_try_displaying_non_exist_job_user_is_recruiter(client):
    example_recruiter_a_from_db = Recruiter.objects.get(name='a')
    client.force_login(example_recruiter_a_from_db.user)
    # job with id=8 does not exist
    response = client.get("/job/8/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/no_such_job.html')


@pytest.mark.django_db
def test_try_displaying_non_exist_job_user_is_not_student_and_not_recruiter(client):
    example_user = User.objects.create_user("username", "password")
    client.force_login(example_user)
    # job with id=10 does not exist
    response = client.get("/job/10/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/no_such_job.html')
