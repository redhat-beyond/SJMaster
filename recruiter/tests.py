import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet

from recruiter.models import Company, Recruiter


@pytest.fixture
def example_company():
    company = Company(name="test_company", description="test_company_description", website_url="test_company_web")
    company.save()
    return company


@pytest.fixture()
def example_user():
    user = User.objects.create_user("test", "testPassword")
    user.save()
    return user


@pytest.fixture
def example_recruiter(example_company, example_user):
    recruiter = Recruiter(user=example_user, name="test_recruiter", company=example_company, email="test@email",
                          phone_number="test_phone")
    recruiter.save()
    return recruiter


@pytest.mark.django_db
def test_get_all_companies_returns_all_companies_as_a_query_set(example_company):
    companies_set = Company.get_all_companies()
    assert isinstance(companies_set, QuerySet)
    assert all(isinstance(company, Company) for company in companies_set)
    assert list(companies_set.values_list("name", "description", "website_url")) == [
        (example_company.name, example_company.description, example_company.website_url)]


@pytest.mark.django_db
def test_get_all_recruiters_of_a_specified_company_returns_all_recruiters_as_a_query_set(example_recruiter,
                                                                                         example_company):
    recruiter_set = example_company.get_all_recruiters_of_a_specified_company()
    assert isinstance(recruiter_set, QuerySet)
    assert all(isinstance(recruiter, Recruiter) for recruiter in recruiter_set)
    assert list(recruiter_set.values_list("user", "name", "company", "email", "phone_number")) == [
        (example_recruiter.user.id, example_recruiter.name, example_recruiter.company.id, example_recruiter.email,
         example_recruiter.phone_number)]
