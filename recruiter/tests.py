import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from recruiter.models import Company, Recruiter


@pytest.fixture()
def example_user():
    user = User.objects.create_user("test", "testPassword")
    user.save()
    return user


@pytest.fixture
def example_recruiter(example_user):
    recruiter = Recruiter(user=example_user, name="test_recruiter",
                          company=Company.objects.get(name="example_company_a"), email="test@email",
                          phone_number="test_phone")
    recruiter.save()
    return recruiter


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
    recruiter_set = Company.get_all_recruiters_of_a_specified_company(Company.objects.get(name="example_company_a"))
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
    example_user_not_recruiter = User.objects.create_user("notrecruiter", "password")
    example_user_not_recruiter.save()
    assert Recruiter.is_recruiter(example_user_not_recruiter.id) is False
    assert Recruiter.is_recruiter(example_recruiter.user.id) is True
