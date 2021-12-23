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
    assert response.context["user_indicator_template"] == "jobboard/student_user_not_applied_indicator.html"
    assertTemplateUsed(response, 'jobboard/job.html', 'jobboard/student_user_not_applied_indicator.html')
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
    assert response.context["user_indicator_template"] == "jobboard/student_user_applied_indicator.html"
    assertTemplateUsed(response, 'jobboard/job.html', 'jobboard/student_user_applied_indicator.html')


@pytest.mark.django_db
def test_student_trying_to_apply_and_test_after_apply(client, example_student_a):
    client.force_login(example_student_a.user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    assert response.context["user_indicator_template"] == "jobboard/student_user_not_applied_indicator.html"
    assertTemplateUsed(response, 'jobboard/job.html', 'jobboard/student_user_not_applied_indicator.html')
    # example_student_a haven't applied to job with id=1 yet
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    # checking if apply_success was rendered
    assertTemplateUsed(response, 'apply_success.html')


@pytest.mark.django_db
def test_student_tries_to_manually_applying_for_job_again(client, example_student_a):
    client.force_login(example_student_a.user)
    # example_student_a haven't applied to job with id=1 yet. Make him directly apply
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    # checking if apply_success was rendered
    assertTemplateUsed(response, 'apply_success.html')
    # checking his application saved by rendering job1 for him again
    response = client.get("/job/1/")
    assert response.context["user_indicator_template"] == "jobboard/student_user_applied_indicator.html"
    assertTemplateUsed(response, 'jobboard/job.html', 'jobboard/student_user_applied_indicator.html')
    # trying to apply again
    response = client.get("/job/1/apply_for_job/")
    assert response.status_code == 200
    assertTemplateUsed(response, 'you_have_already_applied.html')


@pytest.mark.django_db
def test_job_display_to_user_that_is_recruiter_viewing_his_own_job(client):
    example_recruiter_a_from_db = Recruiter.objects.get(name='a')
    job_to_display = Job.objects.get(id=3)
    client.force_login(example_recruiter_a_from_db.user)
    response = client.get("/job/3/")
    # checking job3 was posted by recruiter_a
    assert job_to_display.recruiter.user.id == example_recruiter_a_from_db.user.id
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html', 'recruiter_user_owns_job_indicator.html')
    assert response.context['job_data'] == job_to_display


@pytest.mark.django_db
def test_job_display_to_user_that_is_recruiter_viewing_not_his_own_job(client):
    example_recruiter_a_from_db = Recruiter.objects.get(name='a')
    job_to_display = Job.objects.get(id=2)
    client.force_login(example_recruiter_a_from_db.user)
    response = client.get("/job/2/")
    # checking job2 was not posted by recruiter_a
    assert job_to_display.recruiter.user.id != example_recruiter_a_from_db.user.id
    # checking no other template was included apart from job.html
    assert response.context["user_indicator_template"] is None
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/job.html')
    assert response.context['job_data'] == job_to_display


@pytest.mark.django_db
def test_job_display_to_user_that_is_not_student_and_not_recruiter(client):
    example_user = User.objects.create_user("username", "password")
    client.force_login(example_user)
    response = client.get("/job/1/")
    assert response.status_code == 200
    # checking no other template was included apart from job.html
    assert response.context["user_indicator_template"] is None
    assertTemplateUsed(response, 'jobboard/job.html')
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
