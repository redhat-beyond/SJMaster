import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from pytest_django.asserts import assertTemplateUsed

from recruiter.models import Company, Recruiter
from recruiter.forms import RecuiterRegistrationForm
from jobboard.models import Job
from job_application.models import Application
from student.models import EducationalInstitution, Student
from datetime import date


@pytest.fixture()
def example_user():
    user = User.objects.create_user("yarin", "Y123456789")
    user.save()
    return user


@pytest.fixture
def example_recruiter(example_user):
    recruiter = Recruiter(user=example_user, name="yarin bouzaglo",
                          company=Company.objects.get(name="example_company_a"), email="test@yarin@example.com",
                          phone_number="0524434795")
    recruiter.save()
    return recruiter


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
                           date_of_birth=date(2020, 7, 13),
                           phone_number="0000000000", educational_institution=example_institution,
                           graduation_date=date(2020, 7, 13))
    test_student.save()
    return test_student


@pytest.fixture
def example_job_application(example_student):
    job_a = Job.objects.get(title="job_a")
    application_a = Application(
        job=job_a, student=example_student, date_applied=date(2021, 7, 15))
    application_a.save()
    return application_a


@pytest.fixture
def invalid_recruiters_data():
    # username can't be none
    users_data = [
        {'username': "", 'email': "yarin@example.com",
         'password1': "Y123456789", 'password2': "Y123456789",
         'name': "yarin bouzaglo",
         'company': Company.objects.get(name="example_company_a"),
         "phone_number": "0524434795"},
        # invalid email
        {'username': "", 'email': "yarin",
         'password1': "Y123456789", 'password2': "Y123456789",
         'name': "yarin bouzaglo",
         'company': Company.objects.get(name="example_company_a"),
         "phone_number": "0524434795"},
        # passwords don't match
        {'username': "", 'email': "yarin@example.com",
         'password1': "Y123456789", 'password2': "Y1234",
         'name': "yarin bouzaglo",
         'company': Company.objects.get(name="example_company_a"),
         "phone_number": "0524434795"}, ]
    return users_data


@pytest.fixture
def valid_recruiter_data():
    recruiter_data = {'username': "yarinTest1", 'email': "yarin@example.com",
                      'password1': "Y123456789", 'password2': "Y123456789",
                      'name': "yarin",
                      'company': Company.objects.get(name="example_company_a").id,
                      "phone_number": "0524434795"}
    return recruiter_data


@pytest.mark.django_db
def test_get_all_companies_returns_all_companies_as_a_query_set():
    companies_set = Company.get_all_companies()
    assert isinstance(companies_set, QuerySet)
    assert all(isinstance(company, Company) for company in companies_set)
    assert list(companies_set.values_list("name", "description", "website_url")) == [
        ("example_company_a", "This is company a", "company_a.com"),
        ("example_company_b", "This is company b", "company_b.com")]


@pytest.mark.django_db
def test_get_all_recruiters_of_a_specified_company_returns_all_recruiters_as_a_query_set(example_recruiter):
    recruiter_set = Company.get_all_recruiters_of_a_specified_company(
        Company.objects.get(name="example_company_a"))
    recruiter_a_already_in_db = Recruiter.objects.get(name='a')
    assert isinstance(recruiter_set, QuerySet)
    assert all(isinstance(recruiter, Recruiter) for recruiter in recruiter_set)
    assert list(recruiter_set.values_list("user", "name", "company", "email", "phone_number")) == [
        (recruiter_a_already_in_db.user.id, recruiter_a_already_in_db.name, recruiter_a_already_in_db.company.id,
         recruiter_a_already_in_db.email, recruiter_a_already_in_db.phone_number),
        (example_recruiter.user.id, example_recruiter.name, example_recruiter.company.id, example_recruiter.email,
         example_recruiter.phone_number),
    ]


@pytest.mark.django_db
def test_if_user_is_a_recruiter_returns_true_if_the_auth_user_is_associated_with_a_recruiter_account(example_recruiter):
    example_user_not_recruiter = User.objects.create_user(
        "notrecruiter", "password")
    example_user_not_recruiter.save()
    assert Recruiter.is_recruiter(example_user_not_recruiter.id) is False
    assert Recruiter.is_recruiter(example_recruiter.user.id) is True


@pytest.mark.django_db
def test_get_user_as_recruiter_object(example_recruiter):
    assert isinstance(Recruiter.get_recruiter(
        example_recruiter.user.id), Recruiter)


@pytest.mark.django_db
def test_get_recruiter_raises_exception_for_non_recruiter_user():
    example_user_not_recruiter = User.objects.create_user(
        "notrecruiter", "password")
    example_user_not_recruiter.save()
    with pytest.raises(Recruiter.DoesNotExist):
        Recruiter.get_recruiter(example_user_not_recruiter.id)


@pytest.mark.django_db
def test_sign_up_valid_recruiter(valid_recruiter_data):
    form = RecuiterRegistrationForm(data=valid_recruiter_data)
    if form.is_valid():
        user = form.save()
        assert User.objects.filter(pk=user.user.id).exists()
        assert Recruiter.objects.filter(pk=user).exists()
    else:
        assert False


@pytest.mark.django_db
def test_sign_up_invalid_recruiter(invalid_recruiters_data):
    for user_data in invalid_recruiters_data:
        invalid = False
        form = RecuiterRegistrationForm(data=user_data)
        try:
            form.save()
        except ValueError:
            invalid = True
        assert invalid


@pytest.mark.django_db
def test_signup_form_for_recruiter_loads_correctly(valid_recruiter_data, client):
    response = client.post("/recruiterRegister/")
    assert response.status_code == 200
    form = response.context["form"]
    form_initial_data = response.context["form"].initial
    assert isinstance(form, RecuiterRegistrationForm)
    assert all(form_initial_data[key] == valid_recruiter_data[key] for key in form_initial_data)


@pytest.mark.django_db
def test_new_recruiter_account_with_valid_data(valid_recruiter_data, client):
    response = client.post("/recruiterRegister/", data=valid_recruiter_data)
    assert response.status_code == 302
    user = User.objects.get(username=valid_recruiter_data["username"])
    example_recruiter_from_db = Recruiter.objects.get(user_id=user.id)
    # Test that the new data was updated in the DB
    assert example_recruiter_from_db.email == valid_recruiter_data["email"]
    assert example_recruiter_from_db.name == valid_recruiter_data["name"]
    assert example_recruiter_from_db.phone_number == valid_recruiter_data["phone_number"]


@pytest.mark.django_db
def test_recruiter_my_jobs_loads_correct_data(example_recruiter, example_job_application, client):
    recruiter_object = Recruiter.objects.get(name="a")
    client.force_login(recruiter_object.user)
    response = client.get("/myjobs")
    assert response.status_code == 200
    assertTemplateUsed(response, 'recruiter_my_jobs_and_applications.html')
    jobs_and_applications_from_response = response.context["jobs_and_applications"]
    assert list(jobs_and_applications_from_response.keys()) == list(Job.get_jobs_by_recruiter_id(recruiter_object))
    assert all(
        list(jobs_and_applications_from_response[job]) == list(Application.get_applications_by_job(job)) for job in
        jobs_and_applications_from_response)


@pytest.mark.django_db
def test_student_user_cannot_access_my_jobs_page(example_student, client):
    client.force_login(example_student.user)
    response = client.get("/myjobs")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_not_student_or_recruiter_cannot_access_my_jobs_page(client):
    response = client.get("/myjobs")
    assert response.status_code == 404
