import pytest
from pytest_django.asserts import assertTemplateUsed
from jobboard.models import Job


# The tests use the data that is already in the db from the migration files


@pytest.mark.django_db
def test_search_bar_empty_search(client, example_student_a):
    client.force_login(example_student_a.user)
    search_bar_data = {"searched_name": "", "searched_city": ""}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == set()


@pytest.mark.django_db
def test_search_bar_company(client, example_student_a):
    job_b = Job.objects.get(title="job_b")
    job_d = Job.objects.get(title="job_d")
    client.force_login(example_student_a.user)
    # searches for jobs at 'example_company_b'
    search_bar_data = {"searched_name": "Example_Company_B", "searched_city": ""}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == {job_b, job_d}


@pytest.mark.django_db
def test_search_bar_keyword(client, example_student_a):
    job_a = Job.objects.get(title="job_a")
    job_b = Job.objects.get(title="job_b")
    job_e = Job.objects.get(title="job_e")
    job_sw_microsoft = Job.objects.get(title="Software Engineer Intern")
    client.force_login(example_student_a.user)
    # searches for jobs with keyword 'software'
    search_bar_data = {"searched_name": "software", "searched_city": ""}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == {job_a, job_b, job_e, job_sw_microsoft}


@pytest.mark.django_db
def test_search_bar_by_company_or_keyword_that_dont_have_any_jobs(client, example_student_a):
    client.force_login(example_student_a.user)
    search_bar_data = {"searched_name": "blah", "searched_city": ""}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == set()


@pytest.mark.django_db
def test_search_bar_city(client, example_student_a):
    job_a = Job.objects.get(title="job_a")
    job_c = Job.objects.get(title="job_c")
    job_sw_microsoft = Job.objects.get(title="Software Engineer Intern")
    job_product_manager_apple = Job.objects.get(title="Product manager Intern")
    job_automation_meta = Job.objects.get(title="Automation student")
    job_production_engineer_meta = Job.objects.get(title="Production Engineer student")
    job_backend_engineer_amazon = Job.objects.get(title="Back end intern")
    job_full_stack_intern_amazon = Job.objects.get(title="Full stack intern")
    job_c_developer_intern_monday = Job.objects.get(title="C developer intern")
    client.force_login(example_student_a.user)
    # searches for jobs located at Tel Aviv-Yafo
    search_bar_data = {"searched_name": "", "searched_city": "Tel aviv-yafo"}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == {job_a, job_c, job_sw_microsoft, job_product_manager_apple,
                                                   job_automation_meta, job_production_engineer_meta,
                                                   job_backend_engineer_amazon, job_full_stack_intern_amazon,
                                                   job_c_developer_intern_monday}


@pytest.mark.django_db
def test_search_bar_by_city_that_dont_have_any_jobs(client, example_student_a):
    client.force_login(example_student_a.user)
    search_bar_data = {"searched_name": "", "searched_city": "blah"}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == set()


@pytest.mark.django_db
def test_search_bar_one_company_one_city(client, example_student_a):
    job_e = Job.objects.get(title="job_e")
    client.force_login(example_student_a.user)
    # searches for jobs at 'example_company_a' that are located at Beersheba
    search_bar_data = {"searched_name": "Example_Company_a", "searched_city": "beersheba"}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == {job_e}


@pytest.mark.django_db
def test_search_bar_one_company_one_city_that_dont_have_any_jobs(client, example_student_a):
    client.force_login(example_student_a.user)
    # searches for jobs at 'example_company_a' that are located at Herziliyya
    search_bar_data = {"searched_name": "Example_Company_a", "searched_city": "Herziliyya"}
    response = client.post("/", data=search_bar_data)
    assert response.status_code == 200
    assertTemplateUsed(response, 'jobboard/board.html')
    assert response.context["jobs_to_display"] == set()
