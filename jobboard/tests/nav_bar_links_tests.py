import pytest
from django.contrib.auth.models import User
from recruiter.models import Recruiter

# The tests use the data that is already in the db from the migration files


@pytest.mark.django_db
def test_navbar_links_are_correct_for_student_user(client, example_student_a):
    client.force_login(example_student_a.user)
    response = client.get("/")
    assert response.status_code == 200
    assert response.context['navbar_links'] == {"Account Settings": "/student/account_settings/", "Logout": "/logout",
                                                f"Welcome {example_student_a.user.username}": "#"}


@pytest.mark.django_db
def test_navbar_links_are_correct_for_recruiter_user(client):
    recruiter_user_from_db = Recruiter.objects.get(name='a').user
    client.force_login(recruiter_user_from_db)
    response = client.get("/")
    assert response.status_code == 200
    assert response.context['navbar_links'] == {"Account Settings": "/recruiter/account_settings/",
                                                "My Jobs": "/myjobs",
                                                "Create Job": "/recruiter/create_new_job_form", "Logout": "/logout",
                                                f"Welcome {recruiter_user_from_db.username}": "#"}


@pytest.mark.django_db
def test_navbar_links_are_correct_for_not_logged_in_user(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.context['navbar_links'] == {"Login": "/login"}


@pytest.mark.django_db
def test_navbar_links_are_correct_for_logged_in_user_not_recruiter_or_student(client):
    test_user = User.objects.create_user(username="testuser1", password="testuser1")
    test_user.save()
    client.force_login(test_user)
    response = client.get("/")
    assert response.status_code == 200
    assert response.context['navbar_links'] == {"Logout": "/logout"}
