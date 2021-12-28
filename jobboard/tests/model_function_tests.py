import pytest
from jobboard.models import Job
from student.models import Major
from datetime import date

# The tests use the data that is already in the db from the migration files


@pytest.mark.django_db
def test_get_jobs_by_company_name():
    job_a = Job.objects.get(title="job_a")
    job_c = Job.objects.get(title="job_c")
    job_e = Job.objects.get(title="job_e")
    jobs_by_company_a_name_added_manually = {job_a, job_c, job_e}
    jobs_by_company_a_name_from_test_function = Job.get_jobs_by_company_name("Example_Company_A")
    jobs_by_company_name_that_does_not_exist_from_function = Job.get_jobs_by_company_name("blah")
    assert isinstance(jobs_by_company_a_name_from_test_function, set)
    # tests function with company name "Example_Company_A"
    assert jobs_by_company_a_name_from_test_function == jobs_by_company_a_name_added_manually
    # tests that function with company name that does not exist returns empty set
    assert jobs_by_company_name_that_does_not_exist_from_function == set()


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
    jobs_by_city_name_that_does_not_exist_from_function = Job.get_jobs_by_city_name("blah")
    assert isinstance(jobs_by_city_name_from_test_function, set)
    # tests function with city name "Beersheba"
    assert jobs_by_city_name_from_test_function == jobs_by_city_name_added_manually
    # tests that function with city name that does not exist returns empty set
    assert jobs_by_city_name_that_does_not_exist_from_function == set()


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
def test_get_jobs_by_keyword():
    job_a = Job.objects.get(title="job_a")
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    job_d = Job.objects.get(title="job_d")
    job_e = Job.objects.get(title="job_e")
    jobs_by_keyword_product_added_manually = {job_c, job_d}
    jobs_by_keyword_product_from_function = Job.get_jobs_by_keyword("product")
    jobs_by_keyword_software_added_manually = {job_a, job_b, job_e}
    jobs_by_keyword_software_from_function = Job.get_jobs_by_keyword("Software")
    jobs_by_keyword_that_does_not_exist_from_function = Job.get_jobs_by_keyword("blah")
    # tests function with keyword "product"
    assert jobs_by_keyword_product_from_function == jobs_by_keyword_product_added_manually
    # tests function with keyword "Software"
    assert jobs_by_keyword_software_from_function == jobs_by_keyword_software_added_manually
    # tests that function with keyword that does not exist returns empty set
    assert jobs_by_keyword_that_does_not_exist_from_function == set()


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
