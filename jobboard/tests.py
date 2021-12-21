import pytest
from pytest_django.asserts import assertTemplateUsed
from jobboard.models import Job
from student.models import Major
from datetime import date, timedelta
from django.contrib.auth.models import User
from student.models import Student, EducationalInstitution
from recruiter.models import Recruiter


# The tests use the data that is already in the db from the migration files

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


@pytest.mark.django_db
def test_get_jobs_by_company_name():
    job_a = Job.objects.get(title="job_a")
    job_c = Job.objects.get(title="job_c")
    job_e = Job.objects.get(title="job_e")
    jobs_by_company_a_name_added_manually = {job_a, job_c, job_e}
    jobs_by_company_a_name_from_test_function = Job.get_jobs_by_company_name("example_company_a")
    assert isinstance(jobs_by_company_a_name_from_test_function, set)
    assert jobs_by_company_a_name_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_recruiter_id():
    job_a = Job.objects.get(title="job_a")
    job_c = Job.objects.get(title="job_c")
    jobs_by_recruiter_a_added_manually = {job_a, job_c}
    jobs_by_recruiter_a_id_from_test_function = Job.get_jobs_by_recruiter_id(job_a.recruiter)
    assert isinstance(jobs_by_recruiter_a_added_manually, set)
    assert jobs_by_recruiter_a_id_from_test_function == jobs_by_recruiter_a_added_manually


@pytest.mark.django_db
def test_get_jobs_by_city_name():
    job_b = Job.objects.get(title="job_b")
    job_e = Job.objects.get(title="job_e")
    jobs_by_city_name_added_manually = {job_b, job_e}
    jobs_by_city_name_from_test_function = Job.get_jobs_by_city_name("Beersheba")
    assert isinstance(jobs_by_city_name_from_test_function, set)
    assert jobs_by_city_name_from_test_function == jobs_by_city_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_region_name():
    job_a = Job.objects.get(title="job_a")
    job_c = Job.objects.get(title="job_c")
    job_d = Job.objects.get(title="job_d")
    jobs_by_company_a_name_added_manually = {job_a, job_c, job_d}
    jobs_by_region_name_from_test_function = Job.get_jobs_by_region_name("Tel Aviv")
    assert isinstance(jobs_by_region_name_from_test_function, set)
    assert jobs_by_region_name_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_type():
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    job_e = Job.objects.get(title="job_e")
    jobs_by_company_a_name_added_manually = {job_b, job_c, job_e}
    jobs_by_type_from_test_function = Job.get_jobs_by_job_type("Part-Time")
    assert isinstance(jobs_by_type_from_test_function, set)
    assert jobs_by_type_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_keywords():
    job_a = Job.objects.get(title="job_a")
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    job_d = Job.objects.get(title="job_d")
    job_e = Job.objects.get(title="job_e")
    jobs_by_keyword_product_added_manually = {job_c, job_d}
    jobs_by_keyword_product_from_function = Job.get_jobs_by_keywords("product")
    jobs_by_keywords_software_and_engineer_added_manually = {job_a, job_b, job_e}
    jobs_by_keywords_software_and_engineer_from_function = Job.get_jobs_by_keywords("software", "engineer")
    # tests function with single keyword "product"
    assert jobs_by_keyword_product_from_function == jobs_by_keyword_product_added_manually
    # tests function with 2 keywords "software" and "engineer"
    assert jobs_by_keywords_software_and_engineer_from_function == jobs_by_keywords_software_and_engineer_added_manually


@pytest.mark.django_db
def test_get_jobs_posted_on_or_after_specific_date():
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    job_d = Job.objects.get(title="job_d")
    jobs_created_from_specific_date_added_manually = {job_b, job_c, job_d}
    jobs_created_from_specific_date_from_function = \
        Job.get_jobs_posted_on_or_after_specific_date(date(2021, 7, 15))
    assert jobs_created_from_specific_date_added_manually == jobs_created_from_specific_date_from_function


@pytest.mark.django_db
def test_get_jobs_by_work_model():
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    jobs_by_hybrid_work_model_added_manually = {job_b, job_c}
    jobs_by_hybrid_work_model_from_function = Job.get_jobs_by_work_model("Hybrid")
    assert jobs_by_hybrid_work_model_added_manually == jobs_by_hybrid_work_model_from_function


@pytest.mark.django_db
def test_get_jobs_by_major():
    job_a = Job.objects.get(title="job_a")
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    job_d = Job.objects.get(title="job_d")
    job_e = Job.objects.get(title="job_e")
    jobs_by_communications_major_added_manually = {job_b, job_e}
    jobs_by_communications_major_from_test_function = Job.get_jobs_by_major(Major.COMMUNICATIONS)
    jobs_by_computer_science_and_law_major_added_manually = {job_a, job_c, job_d}
    jobs_by_computer_science_and_law_major_from_test_function = Job.get_jobs_by_major(Major.COMPUTER_SCIENCE, Major.LAW)
    # tests function by single major "Major.COMMUNICATIONS"
    assert jobs_by_communications_major_from_test_function == jobs_by_communications_major_added_manually
    # tests function by two majors "Major.COMPUTER_SCIENCE" and "Major.LAW"
    assert jobs_by_computer_science_and_law_major_from_test_function == \
           jobs_by_computer_science_and_law_major_added_manually


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
