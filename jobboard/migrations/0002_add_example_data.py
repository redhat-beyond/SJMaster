from django.db import migrations, transaction
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('jobboard', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from jobboard.models import Region, JobTitleKeyword, City, Job
        from recruiter.models import Company

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

            City(name="Tel Aviv-Yafo", region=Region.objects.get(name="Tel Aviv")).save()
            City(name="Beersheba", region=Region.objects.get(name="South")).save()
            City(name="Rishon Leziyyon", region=Region.objects.get(name="Central")).save()
            City(name="Herziliyya", region=Region.objects.get(name="Tel Aviv")).save()

            # adding example companies to db
            example_company_a = Company(name="example_company_a", description="This is company a",
                                        website_url="company_a.com")
            example_company_b = Company(name="example_company_b", description="This is company b",
                                        website_url="company_b.com")
            example_company_a.save()
            example_company_b.save()

            # adding example jobs to db
            job_a = Job(title="job_a", company=example_company_a, job_type="Full-Time", work_from="Office_Only",
                        description="This is job a", city=City.objects.get(name="Tel Aviv-Yafo"), address="Rotchild 12",
                        date_created=datetime.date(2021, 6, 8))
            job_a.save()

            job_b = Job(title="job_b", company=example_company_b, job_type="Part-Time", work_from="Hybrid",
                        description="This is job a", city=City.objects.get(name="Beersheba"), address="Herzel 2",
                        date_created=datetime.date(2021, 11, 20))
            job_b.save()

            title_keyword_a = JobTitleKeyword.objects.get(keyword="software")
            title_keyword_b = JobTitleKeyword.objects.get(keyword="engineer")
            job_a.title_keywords.add(title_keyword_a, title_keyword_b)
            job_b.title_keywords.add(title_keyword_a)

    operations = [
        migrations.RunPython(generate_data),
    ]
