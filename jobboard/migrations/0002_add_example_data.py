from django.db import migrations, transaction
import datetime
from student.models import Major


class Migration(migrations.Migration):
    dependencies = [
        ('jobboard', '0005_job_recruiter'),
        ('jobboard', '0006_job_major'),
        ('recruiter', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from jobboard.models import Region, JobTitleKeyword, City, Job
        from recruiter.models import Company, Recruiter
        from django.contrib.auth.models import User

        region_names = [
            "Central",
            "South",
            "North",
            "Tel Aviv",
            "Haifa",
            "Jerusalem"
        ]

        keywords = [
            "software",
            "engineer",
            "product",
            "automation"
        ]

        # adding regions to db
        with transaction.atomic():
            for name in region_names:
                Region(name=name).save()

            # adding job title keywords to db
            for word in keywords:
                JobTitleKeyword(keyword=word).save()

            City(name="Tel Aviv-Yafo",
                 region=Region.objects.get(name="Tel Aviv")).save()
            City(name="Beersheba", region=Region.objects.get(name="South")).save()
            City(name="Rishon Leziyyon",
                 region=Region.objects.get(name="Central")).save()
            City(name="Herziliyya", region=Region.objects.get(
                name="Tel Aviv")).save()

            # adding example companies to db
            example_company_a = Company(name="example_company_a", description="This is company a",
                                        website_url="company_a.com")
            example_company_b = Company(name="example_company_b", description="This is company b",
                                        website_url="company_b.com")
            example_company_a.save()
            example_company_b.save()

            # adding users for creating recruiters
            user_a = User.objects.create_user("a", "a_password")
            user_b = User.objects.create_user("b", "b_password")

            user_a.save()
            user_b.save()

            # adding example recruiters to db
            recruiter_a = Recruiter(user=user_a, name='a',
                                    company=Company.objects.get(name="example_company_a"), email="aaa@email",
                                    phone_number="1223")

            recruiter_b = Recruiter(user=user_b, name='b',
                                    company=Company.objects.get(name="example_company_b"), email="bbb@email",
                                    phone_number="1234")

            recruiter_a.save()
            recruiter_b.save()

            # adding example jobs to db
            job_a = Job(title="job_a", company=example_company_a, recruiter=recruiter_a, major=Major.COMPUTER_SCIENCE,
                        job_type="Full-Time", work_from="Office-Only",
                        description="This is job a", city=City.objects.get(name="Tel Aviv-Yafo"), address="Rotchild 12",
                        date_created=datetime.date(2021, 6, 8))
            job_a.save()

            job_b = Job(title="job_b", company=example_company_b, recruiter=recruiter_b, major=Major.COMMUNICATIONS,
                        job_type="Part-Time", work_from="Hybrid",
                        description="This is job a", city=City.objects.get(name="Beersheba"), address="Herzel 2",
                        date_created=datetime.date(2021, 11, 20))
            job_b.save()

            job_c = Job(title="job_c", company=example_company_a, recruiter=recruiter_a, major=Major.LAW,
                        job_type="Part-Time", work_from="Hybrid",
                        description="This is job c", city=City.objects.get(name="Tel Aviv-Yafo"), address="Rotchild 12",
                        date_created=datetime.date(2021, 7, 22))
            job_c.save()

            job_d = Job(title="job_d", company=example_company_b, recruiter=recruiter_b, major=Major.COMPUTER_SCIENCE,
                        job_type="Internship", work_from="Remote-Only", description="This is job d",
                        city=City.objects.get(name="Herziliyya"),
                        address="Herzel 2", date_created=datetime.date(2021, 10, 29))
            job_d.save()

            job_e = Job(title="job_e", company=example_company_a, recruiter=recruiter_b, major=Major.COMMUNICATIONS,
                        job_type="Part-Time", work_from="Office_Only", description="This is job e",
                        city=City.objects.get(name="Beersheba"), address="Street 3",
                        date_created=datetime.date(2021, 3, 1))
            job_e.save()

            software_keyword = JobTitleKeyword.objects.get(keyword="software")
            engineer_keyword = JobTitleKeyword.objects.get(keyword="engineer")
            product_keyword = JobTitleKeyword.objects.get(keyword="product")
            automation_keyword = JobTitleKeyword.objects.get(
                keyword="automation")

            job_a.title_keywords.add(software_keyword, engineer_keyword)
            job_b.title_keywords.add(software_keyword)
            job_c.title_keywords.add(product_keyword)
            job_d.title_keywords.add(product_keyword)
            job_e.title_keywords.add(software_keyword, automation_keyword)

    operations = [
        migrations.RunPython(generate_data),
    ]
