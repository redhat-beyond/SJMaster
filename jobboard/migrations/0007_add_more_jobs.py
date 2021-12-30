import datetime
from django.db import migrations, transaction

import jobboard
import student
from jobboard.models import Job
from recruiter.models import Recruiter


class Migration(migrations.Migration):
    dependencies = [
        ('jobboard', '0004_alter_job_work_from'),
        ('jobboard', '0006_job_major'),
        ('recruiter', '0003_add_more_example_companies')
    ]

    def generate_data(apps, schema_editor):
        from recruiter.models import Company

        with transaction.atomic():
            jobs = [("Software Engineer Intern", Company.objects.get(name="Microsoft"),
                     student.models.Major.COMPUTER_SCIENCE,
                     Recruiter.objects.get(name="Michal"), 'Part-Time', 'Hybrid',
                     'Looking for a software engineer intern'
                     'with minimum of 3 semesters left. '
                     'knowledge in python is an advantage.',
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"), 'Hashalom 32', datetime.date(2021, 10, 10),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="software")),
                    ("Product manager Intern", Company.objects.get(name="Apple"),
                     student.models.Major.COMPUTER_SCIENCE,
                     Recruiter.objects.get(name="Eldar"), "Part-Time", "Remote-only",
                     "Apple is recruiting an intern product manager"
                     "for a team that develops a new feature"
                     "Minimum of 2 semesters is required",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Shenkin 45', datetime.date(2020, 10, 10),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="product")),
                    ("QA engineer intern", Company.objects.get(name="Red Hat"),
                     student.models.Major.COMPUTER_SCIENCE,
                     Recruiter.objects.get(name="Sivan"), "Full-Time", "Office-only",
                     "Red Hat is recruiting a new QA engineer intern",
                     jobboard.models.City.objects.get(name="Beersheba"),
                     'Shenkin 45', datetime.date(2021, 5, 13),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Automation student", Company.objects.get(name="Meta"),
                     student.models.Major.COMPUTER_SCIENCE,
                     Recruiter.objects.get(name="Ben"), "Part-Time", "Hybrid",
                     "Meta is recruiting a new Automation student",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Rothschild 22', datetime.date(2021, 10, 14),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Production Engineer student", Company.objects.get(name="Meta"),
                     student.models.Major.ELECTRICAL_ENGINEER,
                     Recruiter.objects.get(name="Ben"), "Part-Time", "Internship",
                     "Meta is recruiting a new Production engineer for a summer internship",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Rothschild 22', datetime.date(2021, 10, 14),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Electrical engineer student", Company.objects.get(name="Palo Alto"),
                     student.models.Major.ELECTRICAL_ENGINEER,
                     Recruiter.objects.get(name="Shani"), "Full-Time", "Hybrid",
                     "Palo Alto is recruiting a new electrical engineer student for a full time job",
                     jobboard.models.City.objects.get(name="Herziliyya"),
                     'Einstein 12', datetime.date(2021, 2, 2),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Project manager student", Company.objects.get(name="Wix"),
                     student.models.Major.COMMUNICATIONS,
                     Recruiter.objects.get(name="Guy"), "Full-Time", "Office-Only",
                     "Wix is looking for a new communication student as a project manager",
                     jobboard.models.City.objects.get(name="Beersheba"),
                     'Einstein 12', datetime.date(2021, 3, 3),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="product")),
                    ("Chip developer student", Company.objects.get(name="Intel"),
                     student.models.Major.ELECTRICAL_ENGINEER,
                     Recruiter.objects.get(name="Noam"), "Full-Time", "Office-Only",
                     "Intel is looking for a new chip developer student",
                     jobboard.models.City.objects.get(name="Beersheba"),
                     'Menachem begin 3', datetime.date(2021, 3, 3),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Junior software engineer intern", Company.objects.get(name="Red Hat"),
                     student.models.Major.SOFTWARE_ENGINEER,
                     Recruiter.objects.get(name="Yael"), "Hybrid", "Full-Time",
                     "Red Hat is looking for a new junior software engineer intern",
                     jobboard.models.City.objects.get(name="Beersheba"),
                     'Shenkin 45', datetime.date(2021, 7, 7),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Back end intern", Company.objects.get(name="Amazon"),
                     student.models.Major.SOFTWARE_ENGINEER,
                     Recruiter.objects.get(name="Eden"), "Hybrid", "Part-Time",
                     "Amazon is looking for a new back end enginner intern",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Hashalom 10', datetime.date(2021, 4, 4),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("Full stack intern", Company.objects.get(name="Amazon"),
                     student.models.Major.SOFTWARE_ENGINEER,
                     Recruiter.objects.get(name="Eden"), "Hybrid", "Part-Time",
                     "Amazon is looking for a new Full Stack enginner intern",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Hashalom 10', datetime.date(2021, 4, 4),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer")),
                    ("C developer intern", Company.objects.get(name="Monday"),
                     student.models.Major.ELECTRICAL_ENGINEER,
                     Recruiter.objects.get(name="Din"), "Office-Only", "Part-Time",
                     "Monday is looking for a new C developer intern",
                     jobboard.models.City.objects.get(name="Tel Aviv-Yafo"),
                     'Hashalom 7', datetime.date(2021, 8, 8),
                     jobboard.models.JobTitleKeyword.objects.get(keyword="engineer"))
                    ]

            for title, company, major, recruiter, job_type, work_from, description, city, address, date_created,\
                    title_keywords in jobs:
                job = Job(title=title, company=company, major=major, recruiter=recruiter, job_type=job_type,
                          work_from=work_from,
                          description=description, city=city, address=address,
                          date_created=date_created)
                job.save()
                job.title_keywords.add(title_keywords)

    operations = [
        migrations.RunPython(generate_data),
    ]
