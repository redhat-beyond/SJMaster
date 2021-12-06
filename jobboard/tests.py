import pytest
from jobboard.models import Job
import datetime


# The tests use the data that is already in the db from the migration files

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
        Job.get_jobs_posted_on_or_after_specific_date(datetime.date(2021, 7, 15))
    assert jobs_created_from_specific_date_added_manually == jobs_created_from_specific_date_from_function


@pytest.mark.django_db
def test_get_jobs_by_work_model():
    job_b = Job.objects.get(title="job_b")
    job_c = Job.objects.get(title="job_c")
    jobs_by_hybrid_work_model_added_manually = {job_b, job_c}
    jobs_by_hybrid_work_model_from_function = Job.get_jobs_by_work_model("Hybrid")
    assert jobs_by_hybrid_work_model_added_manually == jobs_by_hybrid_work_model_from_function
