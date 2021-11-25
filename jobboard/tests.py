import pytest
from jobboard.models import Job, JobTitleKeyword, City
from recruiter.models import Company
import datetime


@pytest.fixture
def example_job_c_for_company_a():
    # note that company_a already exists in the db
    job_c = Job(title="job_c", company=Company.objects.get(name="example_company_a"), job_type="Part-Time",
                work_from="Hybrid",
                description="This is job c", city=City.objects.get(name="Tel Aviv-Yafo"), address="Rotchild 12",
                date_created=datetime.date(2021, 7, 22))
    job_c.save()
    title_keyword_a = JobTitleKeyword.objects.get(keyword="product")
    job_c.title_keywords.add(title_keyword_a)
    return job_c


@pytest.fixture
def example_job_e_for_company_a():
    job_e = Job(title="job_e", company=Company.objects.get(name="example_company_a"), job_type="Part-Time",
                work_from="Office_Only", description="This is job e",
                city=City.objects.get(name="Beersheba"), address="Street 3", date_created=datetime.date(2021, 3, 1))
    job_e.save()
    title_keyword_1 = JobTitleKeyword.objects.get(keyword="software")
    title_keyword_2 = JobTitleKeyword.objects.get(keyword="automation")
    job_e.title_keywords.add(title_keyword_1, title_keyword_2)
    return job_e


@pytest.fixture
def example_job_d_for_company_b():
    # note that company_b already exists in the db
    job_d = Job(title="job_d", company=Company.objects.get(name="example_company_b"), job_type="Internship",
                work_from="Remote-Only", description="This is job d", city=City.objects.get(name="Herziliyya"),
                address="Herzel 2", date_created=datetime.date(2021, 10, 29))
    job_d.save()
    title_keyword_1 = JobTitleKeyword.objects.get(keyword="product")
    job_d.title_keywords.add(title_keyword_1)
    return job_d


@pytest.mark.django_db
def test_get_jobs_by_company_name(example_job_c_for_company_a, example_job_e_for_company_a,
                                  example_job_d_for_company_b):
    job_a_already_in_db = Job.objects.get(title="job_a")
    jobs_by_company_a_name_added_manually = {example_job_c_for_company_a, example_job_e_for_company_a,
                                             job_a_already_in_db}
    jobs_by_company_a_name_from_test_function = Job.get_jobs_by_company_name("example_company_a")
    assert isinstance(jobs_by_company_a_name_from_test_function, set)
    assert jobs_by_company_a_name_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_city_name(example_job_c_for_company_a, example_job_e_for_company_a,
                               example_job_d_for_company_b):
    job_b_already_in_db = Job.objects.get(title="job_b")
    jobs_by_city_name_added_manually = {example_job_e_for_company_a, job_b_already_in_db}
    jobs_by_city_name_from_test_function = Job.get_jobs_by_city_name("Beersheba")
    assert isinstance(jobs_by_city_name_from_test_function, set)
    assert jobs_by_city_name_from_test_function == jobs_by_city_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_region_name(example_job_c_for_company_a, example_job_e_for_company_a,
                                 example_job_d_for_company_b):
    job_a_already_in_db = Job.objects.get(title="job_a")
    jobs_by_company_a_name_added_manually = {example_job_c_for_company_a, example_job_d_for_company_b,
                                             job_a_already_in_db}
    jobs_by_region_name_from_test_function = Job.get_jobs_by_region_name("Tel Aviv")
    assert isinstance(jobs_by_region_name_from_test_function, set)
    assert jobs_by_region_name_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_type(example_job_c_for_company_a, example_job_e_for_company_a,
                          example_job_d_for_company_b):
    job_b_already_in_db = Job.objects.get(title="job_b")
    jobs_by_company_a_name_added_manually = {example_job_c_for_company_a, example_job_e_for_company_a,
                                             job_b_already_in_db}
    jobs_by_type_from_test_function = Job.get_jobs_by_job_type("Part-Time")
    assert isinstance(jobs_by_type_from_test_function, set)
    assert jobs_by_type_from_test_function == jobs_by_company_a_name_added_manually


@pytest.mark.django_db
def test_get_jobs_by_keywords(example_job_c_for_company_a, example_job_e_for_company_a,
                              example_job_d_for_company_b):
    job_a_already_in_db = Job.objects.get(title="job_a")
    job_b_already_in_db = Job.objects.get(title="job_b")
    jobs_by_keyword_product_added_manually = {example_job_d_for_company_b, example_job_c_for_company_a}
    jobs_by_keyword_product_from_function = Job.get_jobs_by_keywords("product")
    jobs_by_keywords_software_and_engineer_added_manually = {job_a_already_in_db, job_b_already_in_db,
                                                             example_job_e_for_company_a}
    jobs_by_keywords_software_and_engineer_from_function = Job.get_jobs_by_keywords("software", "engineer")
    # tests function with single keyword "product"
    assert jobs_by_keyword_product_from_function == jobs_by_keyword_product_added_manually
    # tests function with 2 keywords "software" and "engineer"
    assert jobs_by_keywords_software_and_engineer_from_function == jobs_by_keywords_software_and_engineer_added_manually


@pytest.mark.django_db
def test_get_jobs_posted_on_or_after_specific_date(example_job_c_for_company_a, example_job_e_for_company_a,
                                                   example_job_d_for_company_b):
    job_b_already_in_db = Job.objects.get(title="job_b")
    jobs_created_from_specific_date_added_manually = {job_b_already_in_db, example_job_c_for_company_a,
                                                      example_job_d_for_company_b}
    jobs_created_from_specific_date_from_function = \
        Job.get_jobs_posted_on_or_after_specific_date(datetime.date(2021, 7, 15))
    assert jobs_created_from_specific_date_added_manually == jobs_created_from_specific_date_from_function


@pytest.mark.django_db
def test_get_jobs_by_work_model(example_job_c_for_company_a, example_job_e_for_company_a,
                                example_job_d_for_company_b):
    job_b_already_in_db = Job.objects.get(title="job_b")
    jobs_by_hybrid_work_model_added_manually = {job_b_already_in_db, example_job_c_for_company_a}

    jobs_by_hybrid_work_model_from_function = Job.get_jobs_by_work_model("Hybrid")
    assert jobs_by_hybrid_work_model_added_manually == jobs_by_hybrid_work_model_from_function
